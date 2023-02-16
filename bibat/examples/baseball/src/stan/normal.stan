data {
  int<lower=0> N; // items
  array[N] int<lower=0> K; // trials
  array[N] int<lower=0> y; // successes
  array[2] real prior_mu;
  array[2] real prior_tau;
  array[2] real prior_b_K;
  int<lower=0,upper=1> likelihood;
}
transformed data {
  vector[N] log_K = log(to_vector(K));
  vector[N] log_K_std = (log_K - mean(log_K)) / sd(log_K);
}
parameters {
  real mu; // population mean of success log-odds
  real<lower=0> tau; // population sd of success log-odds
  real b_K;
  vector[N] alpha_std; // success log-odds (standardized)
}
model {
  b_K ~ normal(prior_b_K[1], prior_b_K[2]);
  mu ~ normal(prior_mu[1], prior_mu[2]);
  tau ~ normal(prior_tau[1], prior_tau[2]);
  alpha_std ~ normal(0, 1);
  if (likelihood){
    y ~ binomial_logit(K, mu + b_K * log_K_std + tau * alpha_std);
  }
}
generated quantities {
  vector[N] alpha = mu + b_K * log_K_std + tau * alpha_std;
  vector[N] yrep;
  vector[N] llik;
  for (n in 1:N){
    yrep[n] = binomial_rng(K[n], inv_logit(alpha[n]));
    llik[n] = binomial_logit_lpmf(y[n] | K[n], alpha[n]);
  }
}
