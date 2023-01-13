/* Stan program implementing multilevel linear regression. */

functions {
#include custom_functions.stan
}
data {
  int<lower=1> N;
  int<lower=1> N_train;
  int<lower=1> N_test;
  int<lower=1> K;
  matrix[N, K] x;
  vector[N] y;
  array[N_train] int<lower=1,upper=N> ix_train;
  array[N_test] int<lower=1,upper=N> ix_test;
  int<lower=0,upper=1> likelihood;
}
transformed data {
  matrix[N, K] x_std = standardise_cols(x, col_means(x), col_sds(x));
}
parameters {
  real a;
  vector[K] b;
  real<lower=0> sigma;
}
model {
  a ~ normal(0, 1);
  b ~ normal(0, 1);
  sigma ~ lognormal(0, 1);
  if (likelihood){
    y[ix_train] ~ normal_id_glm(x_std[ix_train], a, b, sigma);
  }
}
generated quantities {
  vector[N_test] yrep;
  vector[N_test] llik;
  for (n in 1:N_test){
    yrep[n] = normal_rng(a + x_std[ix_test[n]] * b, sigma);
    llik[n] = normal_lpdf(y[ix_test[n]] | a + x_std[ix_test[n]] * b, sigma);
  }
}
