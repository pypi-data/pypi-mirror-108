# Copyright 2021 Jean-Baptiste Delisle and Lucille Delisle
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from itertools import permutations
import time
from scipy.stats import kde, gamma, nbinom
from scipy.special import factorial, gamma as gammafunc, binom
import pandas as pd
import samsam
import samsam.logprior

# Local imports
from . common import get_prefix_suffix, get_bins_centers

mpl.use('agg')


# Define log probability function
def logprob(p,
            pref, wdist, permutx,
            k, N, temp=1.0):
  # Log prior
  lp = logprior(p, pref, wdist, permutx)
  if np.isfinite(lp):
    # If the parameters are possible
    # Log likelihood
    ll = loglike(p, k, N)
    # Return sum of log prior and log likelihood
    return((lp + ll) / temp)
  else:
    # If the parameters are impossible
    return(-np.inf)


# Define the log prior
def logprior(p, pref, wdist, permutx):
  # Raise exception if one of the condition is not
  # satisfied
  try:
    amp = p[2::3]
    mu = p[::3]
    sig = p[1::3]
    # We complete the list of parameters:
    p_full = np.concatenate(([1 - np.sum(amp)], p))
    amp_full = np.concatenate(([1 - np.sum(amp)], amp))
    # Amplitude
    # Amplitudes should be positive
    if np.any(amp_full < 0):
      raise Exception('Negative amplitude')
    # Because we impose that sum of amplitude is below 1
    # We add this term:
    lp = np.log(factorial(amp.size))
    # Check swapping (symmetry of the problem)
    # pref is a parameter set and we impose that pref
    # is closer to p than any permutation of p
    dp = p - pref
    dist = np.sum(wdist * dp * dp)
    for ks in permutx[1:]:
      dpk = p_full[ks][1:] - pref
      distk = np.sum(wdist * dpk * dpk)
      if distk <= dist:
        raise Exception('Swapping')
    # Number of possible swappings
    lp += np.log(permutx.shape[0])
    # Finally we add the priors on other parameters
    # Location
    lp += sum(samsam.logprior.uniform(muk, 0, 1) for muk in mu)
    # Scale
    lp += sum(samsam.logprior.uniform(sigk, 0, 1) for sigk in sig)
  except:
    return(-np.inf)
  return(lp)


# pdf of gamma
def pdf_gamma(x, mu, sigma):
  return(gamma.pdf(x, mu * mu / (sigma * sigma), 0, sigma * sigma / mu))


# neg binom
def neg_binom_scipy(k, N, mu, sigma):
  return(nbinom(mu * mu / (sigma * sigma),
                1 / (1 + N * sigma * sigma / mu)).pmf(k))


def neg_binom_using_binom(k, N, mu, sigma):
  alpha = (mu / sigma) ** 2
  p = 1 / (1 + mu / (N * sigma ** 2))
  return(binom(k + alpha - 1, k) * p ** k * (1 - p) ** alpha)


def compute_binom_coefs(alpha, kmax):
  k = np.arange(kmax)
  ck = (alpha + k) / (k + 1)
  b = np.empty(kmax + 1)
  b[0] = 1
  np.cumprod(ck, out=b[1:])
  # for k in range(kmax):
  #   b[k + 1] = (alpha + k) / (k + 1) * b[k]
  return(b)


def neg_binom(k, N, mu, sigma):
  alpha = (mu / sigma) ** 2
  b = compute_binom_coefs(alpha, k.max())
  p = 1 / (1 + (mu / sigma ** 2) / N)
  return(b[k] * np.exp(k * np.log(p) + alpha * np.log(1 - p)))

import numpy as np
import time
x = np.linspace(0, 5, 2361)
t0 = time.time()
for _ in range(100000):
  y = (np.e+0*x)**x#np.exp(x*np.log(np.e+0*x))
t1 = time.time()
for _ in range(100000):
  z = np.log(y)
t2 = time.time()
print(t1-t0, t2-t1)

# Log likelihood
def loglike(p, k, N):
  amp = p[2::3]
  mu = p[::3]
  sig = p[1::3]
  amp_full = np.concatenate(([1 - np.sum(amp)], amp))
  likecell = np.zeros(N.size)
  for amp_k, mu_k, sigma_k in zip(amp_full, mu, sig):
    likecell += amp_k * neg_binom(k, N, mu_k, sigma_k)
  # The log likelihood for all cells is
  # sum of log likelihood for each cell
  ll = np.sum(np.log(likecell))
  return(ll)


# Get the pdf 1d using parameters
def get_pdf(p, x):
  amp = p[2::3]
  mu = p[::3]
  sig = p[1::3]
  # We complete the list of parameters:
  amp_full = np.concatenate(([1 - np.sum(amp)], amp))
  pdf = np.zeros(len(x))
  for ampk, muk, sigk in zip(amp_full, mu, sig):
    # Add the gamma
    pdf += ampk * pdf_gamma(x, muk, sigk)
  return(pdf)


# Return the same as gauss_mcmc but from a npz
def extract_from_npz(output):
  print("Reading")
  start = time.time()
  mcmc_res = np.load(output, allow_pickle=True)
  diags = mcmc_res['diagnostics']
  mu = diags.item().get('mu')
  cov = diags.item().get('cov')
  logprob_values = diags.item().get('logprob')
  samples = mcmc_res['samples']
  print(f"Read. It took {(time.time() - start):.2f} seconds.")
  return(mu, cov, logprob_values, samples)


# In order to compare multiple models we use an estimate of the log evidence
def write_evidence(data, col_gene, mu, cov,
                   covis_scale, nis, logprob, output, seed):
  nnorm = (mu.size + 1) // 3
  # Get all UMI nbs:
  N = data['nCount_RNA']
  # Get the raw counts:
  k = data[col_gene]

  # We want to permut the gaussians (3 parameters for each)
  permutx = np.array([np.concatenate(([3 * i + np.arange(3) for i in v]))
                      for v in permutations(np.arange(nnorm))])

  # We calculate logevidence
  np.random.seed(seed)
  logevidence = samsam.covis(mu, covis_scale ** 2 * cov,
                             logprob, nsamples=nis,
                             pref=mu, wdist=1 / (np.diag(cov)), permutx=permutx,
                             k=k, N=N)[2]['logevidence']

  # We write it into a file
  with open(output, 'w') as fo:
    fo.write(f'{logevidence}\n')


def plots_from_pdf(x, pdf, title, output, data, col_gene):
  # Process the output to get prefix and suffix
  file_prefix, file_suffix = get_prefix_suffix(output)

  # 1, 2, 3 sigma:
  qm = np.array([(1 - lvl) / 2 for lvl in [0.6827, 0.9545, 0.9973]])
  qp = 1 - qm

  # Export the pdf mean and 1 sigma (68%) and median
  pdf_summary = pd.DataFrame(columns=['x', 'low', 'mean', 'high', 'median'])
  pdf_summary['x'] = x
  # Plot PDF with 1, 2, 3 sigma
  plt.figure()
  # 1,2,3 sigma
  for i, alpha in enumerate([0.2, 0.1, 0.05]):
    pm = np.quantile(pdf, qm[i], axis=0)
    pp = np.quantile(pdf, qp[i], axis=0)
    if i == 0:
      pdf_summary['low'] = pm
      pdf_summary['high'] = pp
    plt.fill_between(x, pm, pp, color='r', alpha=alpha, rasterized=True)
  # Mean
  plt.plot(x, np.mean(pdf, axis=0), 'r', lw=2, rasterized=True)
  pdf_summary['mean'] = np.mean(pdf, axis=0)
  # Median
  median = np.median(pdf, axis=0)
  pdf_summary['median'] = median
  plt.plot(x, median, 'k--', lw=2, rasterized=True)
  # KDE
  ks = data[col_gene]
  Ns = data['nCount_RNA']
  try:
    density = kde.gaussian_kde(ks / Ns)(x)
    plt.plot(x, density, color='green')
  except Exception:
    print("Could not compute density from input data.")
  plt.ylim(0, )
  plt.xlabel(f'expression')
  plt.ylabel('PDF')
  plt.title(title)
  plt.savefig(output, dpi=300)

  # # Compute the posterior probability of each cell
  # nx = x.size
  # nox = nx * osampx
  # ox = get_bins_centers(xmin, xmax, nox)
  # Ax = get_Ax(data, col_gene, nx, x, dx, ox, xscale, target_sum)
  # post_per_cell = Ax * np.mean(pdf, axis=0)
  # # I renormalize each pdf:
  # post_per_cell /= (np.sum(post_per_cell, axis=1)[:, None] * dx)
  # # I average:
  # post_all_cells = np.mean(post_per_cell, axis=0)
  # # I plot:
  # plt.plot(x, post_all_cells, color='orange')
  # plt.savefig(f'{file_prefix}_with_posterior.{file_suffix}', dpi=300)

  # # Export
  # pdf_summary.to_csv(f'{file_prefix}_pdf.txt',
  #                    index=False,
  #                    header=True, sep='\t')

  # # Plot some individual pdfs
  # colors = plt.cm.jet(np.linspace(0, 1, 100))

  # plt.figure()
  # plt.title(f"{title}\n100 individual samples")
  # for i, cur_pdf in enumerate(pdf[::(pdf.shape[0] // 100)][:100]):
  #   plt.plot(x, cur_pdf, color=colors[i], alpha=0.3, rasterized=True)
  # plt.savefig(f'{file_prefix}_individuals.{file_suffix}')

  # # I plot posterior of first cells:
  # ncells = min(50, post_per_cell.shape[0])
  # colors = plt.cm.jet(np.linspace(0, 1, ncells))
  # plt.figure()
  # plt.title(f"{title}\nposterior of {ncells} cells")
  # for i, cur_pdf in enumerate(post_per_cell[:ncells, :]):
  #   plt.plot(x, cur_pdf, color=colors[i], alpha=0.3, rasterized=True)
  # plt.savefig(f'{file_prefix}_posterior_individuals.{file_suffix}')

  # average_per_cell = np.sum(post_per_cell * x, axis=1) * dx
  # average_square_per_cell = np.sum(post_per_cell * x * x, axis=1) * dx
  # var_per_cell = average_square_per_cell - average_per_cell * average_per_cell
  # infered_pdf_per_cell = np.array([trunc_norm(x, dx, mu, np.sqrt(var)) for mu, var in zip(average_per_cell, var_per_cell)])
  # infered_pdf_global = np.mean(infered_pdf_per_cell, axis=0)
  # # Plot
  # plt.figure()
  # # Mean
  # plt.plot(x, np.mean(pdf, axis=0), 'r', lw=2, rasterized=True, label='baredSC mean pdf')
  # # Median
  # median = np.median(pdf, axis=0)
  # plt.plot(x, median, 'k--', lw=2, rasterized=True, label='baredSC median pdf')
  # # KDE
  # ks = data[col_gene]
  # Ns = data['nCount_RNA']
  # try:
  #   if xscale == 'Seurat':
  #     density = kde.gaussian_kde(np.log(1 + target_sum * ks / Ns))(x)
  #   elif xscale == 'log':
  #     Xs = ks / Ns
  #     # I artificially substitute all 0 by exp(xmin)
  #     Xs[Xs == 0] = np.exp(xmin)
  #     density = kde.gaussian_kde(np.log(Xs))(x)
  #   else:
  #     raise Exception("Only xscale Seurat and log are implemented.")
  #   plt.plot(x, density, color='green', label='density from data')
  # except Exception:
  #   print("Could not compute density from input data.")
  # # Posterior using full pdf
  # plt.plot(x, post_all_cells, color='orange', label='mean post pdf')
  # # Only mean value per cell
  # try:
  #   density = kde.gaussian_kde(average_per_cell)(x)
  #   plt.hist(average_per_cell, bins=40, color='magenta', label='histogram post mean', density=True)
  #   plt.plot(x, density, color='pink', label='density post mean')
  # except Exception:
  #   print("Could not compute density from average per cell.")
  # plt.plot(x, infered_pdf_global, color='purple', label='post gauss each cell')
  # plt.legend()
  # if xmax > 0:
  #   plt.xlim(xmin, 1.2 * xmax)
  # else:
  #   plt.xlim(xmin, xmax + 1)
  # plt.ylim(0, )
  # if xscale == 'Seurat':
  #   plt.xlabel(f'log(1 + {target_sum} * expression)')
  # elif xscale == 'log':
  #   plt.xlabel('log(expression)')
  # plt.ylabel('PDF')
  # plt.title(title)
  # plt.savefig(f'{file_prefix}_posterior_andco.{file_suffix}', dpi=300)

  # # Export the predicted average and sd for each cell
  # per_cell = pd.DataFrame(columns=['mu', 'sd'])
  # per_cell['mu'] = average_per_cell
  # per_cell['sd'] = np.sqrt(var_per_cell)
  # per_cell.to_csv(f'{file_prefix}_posterior_per_cell.txt',
  #                 index=False,
  #                 header=True, sep='\t')

  # # Export values of mean found in each sample
  # means = pdf @ (x * dx)
  # np.savetxt(f'{file_prefix}_means.txt.gz', means)
