import numpy as np
from sage import utils, core
from tqdm.auto import tqdm


class KernelEstimator:
    '''
    Estimate SAGE values by fitting weighted linear model.

    Args:
      model: callable prediction model.
      imputer: for imputing held out values.
      loss: loss function ('mse', 'cross entropy').
    '''
    def __init__(self, model, imputer, loss):
        self.imputer = imputer
        self.loss_fn = utils.get_loss(loss, reduction='none')
        self.model = utils.model_conversion(model, self.loss_fn)

    def __call__(self,
                 X,
                 Y=None,
                 batch_size=512,
                 detect_convergence=True,
                 convergence_threshold=0.05,
                 n_samples=None,
                 verbose=False,
                 bar=False):
        # Determine explanation type.
        if Y is not None:
            explanation_type = 'SAGE'
        else:
            explanation_type = 'Shapley Effects'

        # Verify model.
        N, _ = X.shape
        num_features = self.imputer.num_groups
        X, Y = utils.verify_model_data(self.model, X, Y, self.loss_fn,
                                       batch_size * self.imputer.samples)

        # Weighting kernel.
        weights = [1 / (i * (num_features - i)) for i in range(1, num_features)]
        weights = np.array([weights[0]] + weights + [weights[0]])
        weights = weights / np.sum(weights)

        # Setup.
        beta0 = 0
        N_beta0 = 0
        beta_sum = 0
        N_beta_sum = 0
        A = 0
        b = 0
        N_Ab = 0

        # Sample subsets.
        n_loops = n_samples // batch_size
        for _ in range(n_loops):
            # Sample data.
            mb = np.random.choice(N, batch_size)
            x = X[mb]
            y = Y[mb]

            # Sample subsets.
            S = np.zeros((batch_size, num_features), dtype=bool)
            num_included = np.random.choice(num_features + 1, size=batch_size,
                                            p=weights)
            for row, num in zip(S, num_included):
                inds = np.random.choice(num_features, size=num, replace=False)
                row[inds] = 1

            # Make predictions.
            y_hat = self.model(self.imputer(x, S))
            y_hat = np.mean(y_hat.reshape(
                -1, self.imputer.samples, *y_hat.shape[1:]), axis=1)
            loss = - self.loss_fn(y_hat, y)

            # Store results.
            S = S.astype(float)
            num_included = np.sum(S, axis=1)
            none_included = (num_included == 0)
            all_included = (num_included == num_features)
            some_included = np.logical_and(num_included > 0,
                                           num_included < num_features)

            if np.sum(none_included) > 0:
                N_beta0 += np.sum(none_included)
                beta0 += np.sum(loss[none_included] - beta0) / N_beta0

            if np.sum(all_included) > 0:
                N_beta_sum += np.sum(all_included)
                beta_sum += np.sum(loss[all_included] - beta_sum) / N_beta_sum

            if np.sum(some_included) > 0:
                N_Ab += np.sum(some_included)
                S_relevant = S[some_included]
                loss_relevant = loss[some_included]
                A = A + (np.matmul(S_relevant.T, S_relevant) - A) / N_Ab
                b = b + (np.matmul(S_relevant.T,
                                   loss_relevant[:, np.newaxis]) - b) / N_Ab

        # Calculate SAGE values.
        beta_sum -= beta0
        b_adjusted = b - 0.5 * beta0
        A_inv = np.linalg.inv(A)
        lam = (np.sum(np.matmul(A_inv, b_adjusted)) - beta_sum) / np.sum(A_inv)
        values = np.matmul(A_inv, b_adjusted - lam)
        std = np.zeros(num_features)

        return core.Explanation(np.squeeze(values), std, explanation_type)
