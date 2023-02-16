functions {
#include custom_functions.stan
}
data {
  int<lower=0> N; // items
  array[N] int<lower=0> K; // trials
  array[N] int<lower=0> y; // successes
  real min_alpha; // noone worse than this would be in the dataset
  real max_alpha;
  array[2] real prior_sigma;
  array[2] real prior_k;
  int<lower=0,upper=1> likelihood;
}
parameters {
  real<lower=0.001> sigma; // scale parameter of generalised pareto distribution
  real<lower=-sigma/(max_alpha-min_alpha)> k; // shape parameter of generalised pareto distribution
  vector<lower=min_alpha,upper=max_alpha>[N] alpha; // success log-odds
}
model {
  sigma ~ normal(prior_sigma[1], prior_sigma[2]);
  k ~ normal(prior_k[1], prior_k[2]);
  alpha ~ gpareto(min_alpha, k, sigma);
  if (likelihood){
    y ~ binomial_logit(K, alpha);
  }
}
generated quantities {
  vector[N] yrep;
  vector[N] llik;
  for (n in 1:N){
    yrep[n] = binomial_rng(K[n], inv_logit(alpha[n]));
    llik[n] = binomial_logit_lpmf(y[n] | K[n], alpha[n]);
  }
}
