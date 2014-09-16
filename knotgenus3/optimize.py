from sage.all import MixedIntegerLinearProgram, RR, vector

def optimal_chain(chain, bdry_matrix, solver=None):
    """
    Return homologous chain which minimizes l^1-norm, using the method of
    Dey, Hirani, and Krishnamoorthy.

    The chain returned is guaranteed to be homologous to the given one, and
    to minimize l^1 provided the linear solver (which might use floating point
    calculations) returned an approximate correct answer.  
    """
    n = bdry_matrix.nrows()
    assert len(chain) == n
    P = MixedIntegerLinearProgram(maximization=False, solver=solver)
    x_plus = P.new_variable(real=True, nonnegative=True)
    x_minus = P.new_variable(real=True, nonnegative=True)
    b = P.new_variable(real=True, nonnegative=False)

    for i, row in enumerate(bdry_matrix.rows()):
        constraint = chain[i]
        for j in row.nonzero_positions():
            constraint += b[j]*row[j]
        P.add_constraint(constraint == x_plus[i] - x_minus[i])

    P.set_objective(sum(x_minus[i] + x_plus[i] for i in range(n)))

    # Lift solution back to Z; do this by rounding the coefficients
    # b of the columns of bdry_matrix; this way, whatever we
    # return must be homologous to the given chain.
    
    min_norm = P.solve()
    b_ans = P.get_values(b)
    b_ans = [RR(b_ans[j]).round() for j in range(bdry_matrix.ncols())]
    ans = chain + bdry_matrix*vector(b_ans)
    assert abs(ans.norm(1) - min_norm) < 0.001
    return ans
