/* This file is for your stan functions */

real gpareto_lpdf(vector y, real ymin, real k, real sigma) {
  // generalised Pareto log pdf
  int N = rows(y);
  real inv_k = inv(k);
  if (k<0 && max(y-ymin)/sigma > -inv_k)
    reject("k<0 and max(y-ymin)/sigma > -1/k; found k, sigma =", k, ", ", sigma);
  if (sigma<=0)
    reject("sigma<=0; found sigma =", sigma);
  if (fabs(k) > 1e-15)
    return -(1+inv_k)*sum(log1p((y-ymin) * (k/sigma))) -N*log(sigma);
  else
    return -sum(y-ymin)/sigma -N*log(sigma); // limit k->0
}
vector standardise_vector(vector v, real mu, real s){
    return (v - mu) / (2 * s);
}

matrix standardise_cols(matrix m, vector mu, vector s){
  matrix[rows(m), cols(m)] out;
  for (c in 1:cols(m))
    out[,c] = standardise_vector(m[,c], mu[c], s[c]);
  return out;
}

vector unstandardise_vector(vector v, real m, real s){
  return m + v * 2 * s;
}

vector col_means(matrix m){
  int C = cols(m);
  vector[C] out;
  for (c in 1:C)
    out[c] = mean(m[,c]);
  return out;
}

vector col_sds(matrix m){
  int C = cols(m);
  vector[C] out;
  for (c in 1:C)
    out[c] = sd(m[,c]);
  return out;
}
