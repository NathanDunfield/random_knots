/*

Magma code for computing the Alexander polynomial of a finitely
presented group.  

By Nathan Dunfield 

This code is released into the public domain. 

The main function is AlexanderPolynomial used like this

> load "alexander.magma";
> G := Group < a,b,c | a^3*c*b^3*a^-1*c^2*b^-1, a^2*c^3*b^2 >;
> AbelianQuotientInvariants(G);
[ 0, 0 ]
> p, R<x,y> := AlexanderPolynomial(G);
> p;
x^8*y^2 + x^7*y^3 + x^6*y^4 + x^6*y^2 + x^6*y + x^5*y^3 + x^5*y^2 + x^4*y^4 + x^4*y^3 + x^4*y^2 + x^4*y + x^4 + x^3*y^2 + x^3*y + x^2*y^3 + 
    x^2*y^2 + x^2 + x*y + y^2

*/

/* Generic function programming goodness */

FoldList := function(f, L)
   return [ i gt 1 select f(Self(i - 1), L[i]) else L[1] : i in [1..#L]];
end function;

Fold := function(f, L)
   ans := FoldList(f, L); return ans[#ans];
end function;

Total := function(L)
   return  #L gt 0 select &+L else 0;     
end function;

Product := function(L)
   return  #L gt 0 select &*L else 1;      
end function;

Concatenation := function(L)
   return #L gt 0 select &cat L else [];
end function;

Last := function(L)
    return L[#L];
end function;

Flatten := function(L)
   if #L eq 0 then return []; end if;
   if #L eq 1 then return L[1]; end if;
   return Fold(function(a,b) return a cat b; end function , L);
end function;

FlattenMatrix := function(M)
   return Flatten(RowSequence(M));
end function;

TailSeq := function(L)
    return [L[i] : i in [2..#L]];
end function;

/* 

Commands for Fox derivatives 

*/

/* 

Returns phi: G -> A = FreeAbQuo(G) as a pair (A, phi);

*/

FreeAbelianQuotientOfGroup := function(G)
   A, g := AbelianQuotient(G);
   fA, f := FreeAbelianQuotient(A);
   phi := g*f;
   assert #Relations(fA) eq 0;
   return fA, phi;
end function;

/* 

If we think of the GroupRing as Laurant polynomials, this function
just clears the denominators, moreover normalizing so that the is a
constant term w.r.t to each variable.  .

*/

GroupRingElementToPolyRing := function(elt, P)
   if IsZero(elt) then return Zero(P); end if;
   parts := [ <x[1], Eltseq(x[2])> : x in Eltseq(elt)];
   exps := Transpose(Matrix([ p[2] : p in parts]));
   minexps := [Minimum(L) : L in RowSequence(exps)];
   exps := Transpose(exps + Matrix([[ -m : i in [1..#parts]] : m in minexps]));
   return Total( [ parts[i][1] * Product([P.j^exps[i][j] : j in [1..Rank(P)]])  : i in [1..#parts]]);
end function;


/* 

Computes the Fox derivative dW/dvar w.r.t to the abelian quotient phi

W should be in Eltseq form, e.g. x*y*X*Y -> [1,2,-1,-2]

*/

FoxSetup := function(G, R, phi, var)
    gen_ims := AssociativeArray();
    fox := AssociativeArray();
    for i in [1..#Generators(G)] do
	gen_ims[i] := R ! phi(G.i);
	gen_ims[-i] := R ! phi(G.i^-1);
	fox[i] := Zero(R);
        fox[-i] := Zero(R);
    end for;
    fox[var] := One(R);
    fox[-var] := -gen_ims[-var];
    return gen_ims, fox;
end function;

FoxDerivative := function(G, R, W, phi, var)
    ans := Zero(R);
    gen_ims, fox:= FoxSetup(G, R, phi, var);
    for w in Reverse(W) do 
	ans := fox[w] + gen_ims[w]*ans;
    end for; 
    return ans;
end function;

/* 

Computes the Alexander polynomial of G w.r.t. the given homomophism
phi: G -> A.  For some reason I don't understand, one needs to pass A
insead of just taking A := Image(phi).

*/

BasicAlexanderPolynomialOfHomomorphism := function(G, A, phi)
   R := GroupAlgebra(Integers(), A);
   P := PolynomialRing(Integers(), #Generators(A));
   s := #Generators(G);
   rels := [ Eltseq(LHS(r) * RHS(r)^-1) : r in Relations(G)];
  M := Matrix( [[FoxDerivative(G, R, r, phi, var)  : r in rels] : var in [1..s]]);
   return GCD([ GroupRingElementToPolyRing(p, P) : p in Minors( M, s - 1)]), P, phi;
end function;

BasicAlexanderPolynomial := function(G)
   A, phi:= FreeAbelianQuotientOfGroup(G);
   return BasicAlexanderPolynomialOfHomomorphism(G, A, phi);
end function;

/*

To make computing the Alexander polynomial faster, we need the
matrix we take the determinant of to be a matrix of polynomials, not
elements of a group ring.

*/

ColumnMinimums := function(M)
   return [Minimum(L) : L in RowSequence(Transpose(Matrix(M)))];
end function;

LaurantExponents := function(elt)
      return [Eltseq(x[2]) : x in Eltseq(elt)];
end function;

MinimumExponents := function(elts)
   exponents := Concatenation([LaurantExponents(elt) : elt in elts | not IsZero(elt)]);
   return ColumnMinimums(exponents);
end function;

ConvertLaurantToPoly := function(elt, expshift, P)
   if IsZero(elt) then return Zero(P); end if;
   parts := [ <x[1], Eltseq(x[2])> : x in Eltseq(elt)];
   exps := Transpose(Matrix([ p[2] : p in parts]));
   exps := Transpose(exps + Matrix([[ m : i in [1..#parts]] : m in expshift]));
   return Total( [ parts[i][1] * Product([P.j^exps[i][j] : j in [1..Rank(P)]])  : i in [1..#parts]]);
end function;
  
GroupRingMatrixToPolyMatrix := function(M, P) // M = matrix, P = polynomial ring
   if IsZero(M) then return Matrix(P, M); end if;
   expshift := [-x : x in MinimumExponents(FlattenMatrix(M))];
   return Matrix(P, [ [ConvertLaurantToPoly(elt, expshift, P) : elt in R] : R in RowSequence(M)]);
end function;

NormalizePolynomialByLaurantUnits := function(poly)
   exponents :=[Exponents(x) : x in Terms(poly)];
   minexp :=  ColumnMinimums(exponents);
   P := Parent(poly);
   return poly div Product([P.j^minexp[j] : j in [1..Rank(P)]]);
end function;



intrinsic AlexanderPolynomialOfHomomorphism(G::GrpFP, A::GrpAb, phi::Map) 
     -> RngMPolElt, RngMPol, Map
{The alexander polynomial of G with respect to the homomorphism phi: G -> A}

   R := GroupAlgebra(Integers(), A);
   P := PolynomialRing(Integers(), #Generators(A));
   s := #Generators(G);
   rels := [ Eltseq(LHS(r) * RHS(r)^-1) : r in Relations(G)];
   foxes :=  [[FoxDerivative(G, R, r, phi, var)  : r in rels] : var in [1..s]];
   M := GroupRingMatrixToPolyMatrix(Matrix(foxes), P);
   minors := Minors( M, s - 1);
   alex := GCD(minors);
   return NormalizePolynomialByLaurantUnits(alex), P, phi;
end intrinsic;



intrinsic AlexanderPolynomial(G::GrpFP) -> RngMPolElt, RngMPol, Map
{The alexander polynomial of the given group}

   A, phi:= FreeAbelianQuotientOfGroup(G);
   return AlexanderPolynomialOfHomomorphism(G, A, phi);
end intrinsic;

/* Some additional code for specifying homomorphisms */

/*

Let G be a group generated by G.1,...,G.n.  Suppose that we are given
a basis for a subspace of H^1(G; Z) in the form of 

  phi_j : G -> Z 

specified by lists [phi_j(G.i)].  The main function below constructs an
explicit homomorphism 

   G -> A

*/

AbelianQuotientFromCohomologyClasses := function(G, phis)
     N := #phis;
     A := AbelianGroup([0 : i in [1..N]]);   
     phi := hom<G -> A | [ Total( [phis[i,j]*A.i : i in [1..N]] ) : j in [1..#Generators(G)]]>;
     assert not false in [ phi(RHS(rel)) eq phi(LHS(rel)) : rel in Relations(G)];
     return A, phi;
end function;

/* 

Note: The following function simplifies the presentation first
computing the Alexander polynomial.

*/

AlexanderPolynomialFromCohomologyClasses := function(G, phis)
     A, phi := AbelianQuotientFromCohomologyClasses(G, phis);
     return AlexanderPolynomialOfHomomorphism(Simplify(G), A, phi);
end function;



