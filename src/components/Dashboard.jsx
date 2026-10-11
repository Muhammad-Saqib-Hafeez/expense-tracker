import { useState, useEffect, useMemo } from 'react';
import { Summary } from './Summary';
import { TransactionForm } from './TransactionForm';
import { TransactionList } from './TransactionList';
import { TransactionFilters } from './TransactionFilters';
import { transactionApi } from '../api/transactions';

export function Dashboard() {
  const [transactions, setTransactions] = useState([]);
  const [filters, setFilters] = useState({ type: 'all', category: 'all' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch transactions on mount
  useEffect(() => {
    loadTransactions();
  }, []);

  const loadTransactions = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await transactionApi.getAll();
      setTransactions(data);
    } catch (err) {
      setError(err.message);
      // Fallback to empty array for demo
      setTransactions([]);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTransaction = async (transaction) => {
    try {
      const newTransaction = await transactionApi.create(transaction);
      setTransactions(prev => [...prev, newTransaction]);
    } catch (err) {
      setError(err.message);
      // For demo, add locally if API fails
      setTransactions(prev => [...prev, transaction]);
    }
  };

  const handleDeleteTransaction = async (id) => {
    try {
      await transactionApi.delete(id);
      setTransactions(prev => prev.filter(t => t.id !== id));
    } catch (err) {
      setError(err.message);
      // For demo, delete locally if API fails
      setTransactions(prev => prev.filter(t => t.id !== id));
    }
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
  };

  const filteredTransactions = useMemo(() => {
    return transactions.filter(t => {
      const typeMatch = filters.type === 'all' || t.type === filters.type;
      const categoryMatch = filters.category === 'all' || t.category === filters.category;
      return typeMatch && categoryMatch;
    });
  }, [transactions, filters]);

  const totals = useMemo(() => {
    const totalIncome = transactions
      .filter(t => t.type === 'income')
      .reduce((sum, t) => sum + t.amount, 0);
    const totalExpenses = transactions
      .filter(t => t.type === 'expense')
      .reduce((sum, t) => sum + t.amount, 0);
    return { totalIncome, totalExpenses, balance: totalIncome - totalExpenses };
  }, [transactions]);

  if (loading) {
    return (
      <div className="loading-screen" role="status" aria-label="Loading">
        <div className="spinner"></div>
        <p>Loading transactions...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <p>Track your income and expenses</p>
      </div>

      {error && (
        <div className="auth-error" style={{ marginBottom: '24px' }}>
          {error}
        </div>
      )}

      <Summary
        totalIncome={totals.totalIncome}
        totalExpenses={totals.totalExpenses}
        balance={totals.balance}
      />

      <TransactionForm onAdd={handleAddTransaction} />

      <TransactionList
        transactions={filteredTransactions}
        onDelete={handleDeleteTransaction}
      />

      <TransactionFilters
        transactions={transactions}
        onFilterChange={handleFilterChange}
      />
    </div>
  );
}