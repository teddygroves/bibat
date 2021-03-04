/* A template for your custom Stan model */
functions {
#include custom_functions.stan
}
data {
  int<lower=1> N;
  int<lower=1> K;
  matrix[N, K] x;
  vector[N] y;
  int<lower=1> N_test;
  matrix[N_test, K] x_test;
  vector[N_test] y_test;
  vector[2] prior_a;
  matrix[K, 2] prior_b;
  vector[2] prior_sigma;
  int<lower=0,upper=1> likelihood;
}
transformed data {
  matrix[N, K] x_std = standardise_cols(x, col_means(x), col_sds(x));
  matrix[N_test, K] x_test_std = standardise_cols(x_test, col_means(x), col_sds(x));
}
parameters {
  real a;
  vector[K] b;
  real<lower=0> sigma;
}
model {
  a ~ normal(prior_a[1], prior_a[2]);
  b ~ normal(prior_b[,1], prior_b[,2]);
  sigma ~ lognormal(prior_sigma[1], prior_sigma[2]);
  if (likelihood){
    y ~ normal_id_glm(x_std, a, b, sigma);
  }
}
generated quantities {
  vector[N_test] yrep;
  vector[N_test] llik;
  for (n in 1:N_test){
    yrep[n] = normal_rng(a + x_test_std[n] * b, sigma);
    llik[n] = normal_lpdf(y_test[n] | a + x_test_std[n] * b, sigma);
  }
}
