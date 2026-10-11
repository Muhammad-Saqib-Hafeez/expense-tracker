import { api } from '../api/client';

export const transactionApi = {
  async getAll() {
    return api.getTransactions();
  },

  async create(transaction) {
    return api.createTransaction(transaction);
  },

  async delete(id) {
    return api.deleteTransaction(id);
  },
};

export const categoryApi = {
  async getAll() {
    return api.request('/categories');
  },

  async create(category) {
    return api.request('/categories', {
      method: 'POST',
      body: JSON.stringify(category),
    });
  },
};