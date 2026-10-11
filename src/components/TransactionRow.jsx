export function TransactionRow({ transaction, onDelete }) {
  const formattedAmount = transaction.amount.toFixed(2);
  const isIncome = transaction.type === 'income';

  return (
    <tr className={isIncome ? 'income-row' : 'expense-row'}>
      <td>{transaction.date}</td>
      <td>{transaction.description}</td>
      <td>
        <span className="category-badge">
          {transaction.category.charAt(0).toUpperCase() + transaction.category.slice(1)}
        </span>
      </td>
      <td>
        <span className={`type-badge ${transaction.type}`}>
          {transaction.type.charAt(0).toUpperCase() + transaction.type.slice(1)}
        </span>
      </td>
      <td className={isIncome ? 'income-amount' : 'expense-amount'}>
        {isIncome ? '+' : '-'}${formattedAmount}
      </td>
      <td>
        <button
          className="btn-delete"
          onClick={() => onDelete(transaction.id)}
          aria-label="Delete transaction"
        >
          ×
        </button>
      </td>
    </tr>
  );
}