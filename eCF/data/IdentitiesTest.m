(* {"RamanujanTauTheta", 1}*)
ConditionalExpression[RamanujanTauTheta[z] == (z*(137/60 - EulerGamma - Log[2*Pi]))/(1 + Inactive[ContinuedFractionK][((-1)^k*z^2*PolyGamma[2*k, 6])/((1 + 2*k)!*(KroneckerDelta[1 - k]*Log[2*Pi] + ((-1)^k*PolyGamma[2*(-1 + k), 6])/(-1 + 2*k)!)), 1 - ((-1)^k*z^2*PolyGamma[2*k, 6])/((1 + 2*k)!*(KroneckerDelta[1 - k]*Log[2*Pi] + ((-1)^k*PolyGamma[2*(-1 + k), 6])/(-1 + 2*k)!)), {k, 1, Infinity}]), Element[z, Complexes] && Abs[z] < 1]

(* {"Sinc", 1}*)
ConditionalExpression[Sinc[z] == (1 + Inactive[ContinuedFractionK][z^2/(2*k*(1 + 2*k)), 1 - z^2/(2*k*(1 + 2*k)), {k, 1, Infinity}])^(-1), Element[z, Complexes]]

(* {"RiemannSiegelTheta", 1}*)
ConditionalExpression[RiemannSiegelTheta[z] == -(z*(Log[Pi] - PolyGamma[0, 1/4]))/2 - (z^3*PolyGamma[2, 1/4])/(48*(1 + Inactive[ContinuedFractionK][(z^2*PolyGamma[2*(1 + k), 1/4])/(8*(3 + 5*k + 2*k^2)*PolyGamma[2*k, 1/4]), 1 - (z^2*PolyGamma[2*(1 + k), 1/4])/(8*(3 + 5*k + 2*k^2)*PolyGamma[2*k, 1/4]), {k, 1, Infinity}])), Element[z, Complexes] && Abs[z] < 1/2]