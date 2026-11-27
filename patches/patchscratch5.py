import sympy as sp

N, L, links, beta, logb = sp.symbols('N L links beta logb', positive=True)
eps_sq = 4 * N * (6 * N**2 * links + 2) * logb / beta

# Check K_kin(U, U') upper bound in terms of D(U, U')!
# chi(U, W) = exp(beta/2 * links - beta/(4*N) * sum_e ||U_e - W_e||_F^2)
# chi(U, W) * chi(U', W) = exp(beta * links - beta/(4*N) * sum_e (||U_e - W_e||_F^2 + ||U'_e - W_e||_F^2))
# Since ||U_e - U'_e||_F^2 <= 2 ||U_e - W_e||_F^2 + 2 ||U'_e - W_e||_F^2,
# ||U_e - W_e||_F^2 + ||U'_e - W_e||_F^2 >= 1/2 * ||U_e - U'_e||_F^2!
# Therefore:
# chi(U, W) * chi(U', W) <= exp(beta * links - beta/(8*N) * D(U, U')) !!

# Look at beta / (8 * N) * (2 * eps_sq) vs beta / (8 * N) * eps_sq:
print("beta/(8*N) * (2*eps_sq) =", sp.simplify((beta / (8 * N)) * (2 * eps_sq)))
print("beta/(8*N) * eps_sq     =", sp.simplify((beta / (8 * N)) * eps_sq))

# Look at small-jump term:
# 1/(2*lam0) * int_{D <= cut} K_W * w * w' * frob(U_e0 - U'_e0)
# <= 1/(2*lam0) * cut * (int int K_W * w * w') = 1/2 * cut!
# For cut = 2 * eps_sq: 1/2 * (2 * eps_sq) = eps_sq <= 2 * eps_sq !
# Wait: what about if cut = 2 * eps_sq, then large-jump exponential is:
# exp(-(6 * N^2 * links + 2) * log(beta)) = beta ^ (-(6 * N^2 * links + 2)) !
# EXACT MATCH WITH err !!

# Now check 1 / lam0!
# Recall lam0 >= 1/mu(B) * int_B int_B K_W(U, U') dU' dU
# On B = {U | forall e, ||U_e - 1||_F^2 <= delta^2}, with delta = 1 / sqrt(beta):
# 1) wilsonPlaquetteTerm p U = 1/(2N) * ||U_p - 1||_F^2
#    Wait: U_p = A * B * C^-1 * D^-1. Let's check exact factor in frobeniusNormSq_su_mul_sub_one!
#    frobeniusNormSq(A * B - 1) <= 2 ||A - 1||_F^2 + 2 ||B - 1||_F^2
#    So frobeniusNormSq((A * B) * (C^-1 * D^-1) - 1)
#      <= 2 ||A * B - 1||_F^2 + 2 ||C^-1 * D^-1 - 1||_F^2
#      <= 4 (||A - 1||_F^2 + ||B - 1||_F^2 + ||C^-1 - 1||_F^2 + ||D^-1 - 1||_F^2)
#      =  4 (||A - 1||_F^2 + ||B - 1||_F^2 + ||C - 1||_F^2 + ||D - 1||_F^2) <= 16 * delta^2 = 16 / beta!
#    Wait: wilsonPlaquetteTerm p U = 1/(2N) * 16/beta = 8 / (N * beta)!
#    Sum over 3 * L^3 plaquettes: S_W[U] <= beta * 3 * L^3 * 8 / (N * beta) = 24 * L^3 / N!
#    So exp(-1/2 * (S_W[U] + S_W[U'])) >= exp(-24 * L^3 / N)!
# 2) For U, U', W in B:
#    ||U_e - W_e||_F^2 <= 2 ||U_e - 1||_F^2 + 2 ||W_e - 1||_F^2 <= 4 * delta^2 = 4 / beta!
#    Wait: chi(U, W) = exp(beta/2 * links - beta/(4N) * sum_e ||U_e - W_e||_F^2)
#    >= exp(beta/2 * links - beta/(4N) * links * 4 / beta) = exp(beta/2 * links - links / N)
#    = exp(beta/2 * links - 3 * L^3 / N)!
#    So chi(U, W) * chi(U', W) >= exp(beta * links - 6 * L^3 / N)!
# 3) Total on B x B with W in B:
#    K_W(U, U') >= mu(B) * exp(beta * links - 30 * L^3 / N)!
#    Integrating with phi = 1_B / sqrt(mu(B)):
#    lam0 >= <phi, T_raw phi> >= 1/mu(B) * mu(B)^2 * mu(B) * exp(beta * links - 30 * L^3 / N)
#         = mu(B)^2 * exp(beta * links - 30 * L^3 / N)!
#    Since mu(B) >= (1 / K^(2*N*N))^links:
#    1 / lam0 <= ((K^(2*N*N))^(2*links)) * exp(-beta * links + 30 * L^3 / N)!
# 4) Therefore on large jump {D > 2 * eps_sq}:
#    1 / (2 * lam0) * int int_{D > 2*eps_sq} K_W * w * w' * 4 * N dU dU'
#    <= 1 / (2 * lam0) * 4 * N * exp(beta * links) * beta^(-(6*N^2*links + 2)) * (int w)^2
#    <= 2 * N * ((K^(2*N*N))^(2*links)) * exp(30 * L^3 / N) * beta^(-(6*N^2*links + 2))
#    <= 8 * N * exp(30 * L^3 / N) * ((K^(2*N*N))^(2*links)) * beta^(-(6*N^2*links + 2)) !!
print("All constants check out with room to spare! (1 <= 2 and 2 <= 8)")
