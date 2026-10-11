import { TransactionRow } from './TransactionRow';
import { TransactionFilters } from './TransactionFilters';

export function TransactionList({ transactions, onDelete }) {
  return (
    <div className="transactions">
      <h2>Transactions</h2>
      <TransactionFilters />
      <table className="transactions-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Description</th>
            <th>Category</th>
            <th>Type</th>
            <th>Amount</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {transactions.length === 0 ? (
            <tr>
              <td colSpan="6" className="empty-state">No transactions found</td>
            </tr>
          ) : (
            transactions.map(transaction => (
              <TransactionRow
                key={transaction.id}
                transaction={transaction}
                onDelete={onDelete}
              />
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}