import os
import numpy as np
import tempfile
import unittest
from GPT_linear_regressor.linear_regressor import Dataset, LinearRegressor


class TestDataset(unittest.TestCase):

    def setUp(self):
        self.dataset = Dataset()
        self.array = np.array([[1, 2], [2, 4], [3, 6], [4, 8]])
        self.csv_path = os.path.join(tempfile.gettempdir(), "test.csv")
        np.savetxt(self.csv_path, self.array, delimiter=',')

    def tearDown(self):
        os.remove(self.csv_path)

    def test_from_csv(self):
        self.dataset.from_csv(self.csv_path)
        np.testing.assert_array_equal(self.dataset.data, self.array)

    def test_from_numpy(self):
        self.dataset.from_numpy(self.array)
        np.testing.assert_array_equal(self.dataset.data, self.array)

    def test_test_train_split(self):
        self.dataset.from_numpy(self.array)
        self.dataset.test_train_split(pct_test=0.5)
        np.testing.assert_array_equal(self.dataset.X_train, np.array([1, 2]))
        np.testing.assert_array_equal(self.dataset.X_test, np.array([3, 4]))
        np.testing.assert_array_equal(self.dataset.y_train, np.array([2, 4]))
        np.testing.assert_array_equal(self.dataset.y_test, np.array([6, 8]))


class TestLinearRegressor(unittest.TestCase):

    def setUp(self):
        self.dataset = Dataset()
        self.array = np.array([[1, 2], [2, 4], [3, 6], [4, 8]])
        self.dataset.from_numpy(self.array)
        self.dataset.test_train_split(pct_test=0.5)
        self.regressor = LinearRegressor(self.dataset)

    # GPT makes incorrect changes to test_train, but correctly changes rtol to atol. Also cannot infer thetas dimension.
    def test_train(self):
        self.regressor.train()
        np.testing.assert_allclose(self.regressor.thetas, np.array([[0], [2]]), atol=1e-5)

    def test_predict(self):
        self.regressor.train()
        predictions_test = self.regressor.predict(test=True)
        np.testing.assert_allclose(predictions_test, np.array([[6], [8]]), rtol=1e-5)
        predictions_train = self.regressor.predict(test=False)
        np.testing.assert_allclose(predictions_train, np.array([[2], [4]]), rtol=1e-5)

    def test_score(self):
        self.regressor.train()
        score_test = self.regressor.score(test=True)
        self.assertAlmostEqual(score_test, 1.0, places=5)
        score_train = self.regressor.score(test=False)
        self.assertAlmostEqual(score_train, 1.0, places=5)

    # GPT makes the same mistake here as with test_train.
    def test_save_coeffs(self):
        self.regressor.train()
        filename = os.path.join(tempfile.gettempdir(), "coeffs")
        self.regressor.save_coeffs(filename)
        loaded_thetas = np.load(f'{filename}.npy')
        np.testing.assert_allclose(loaded_thetas, np.array([[0], [2]]), atol=1e-5)
        os.remove(f'{filename}.npy')


if __name__ == '__main__':
    unittest.main()
