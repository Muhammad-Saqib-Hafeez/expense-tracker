import { useState } from 'react';

const categories = ["food", "housing", "utilities", "transport", "entertainment", "salary", "other"];

export function TransactionFilters({ onFilterChange }) {
  const [filterType, setFilterType] = useState("all");
  const [filterCategory, setFilterCategory] = useState("all");

  const handleTypeChange = (e) => {
    const value = e.target.value;
    setFilterType(value);
    onFilterChange({ type: value, category: filterCategory });
  };

  const handleCategoryChange = (e) => {
    const value = e.target.value;
    setFilterCategory(value);
    onFilterChange({ type: filterType, category: value });
  };

  return (
    <div className="filters">
      <select value={filterType} onChange={handleTypeChange} aria-label="Filter by type">
        <option value="all">All Types</option>
        <option value="income">Income</option>
        <option value="expense">Expense</option>
      </select>
      <select value={filterCategory} onChange={handleCategoryChange} aria-label="Filter by category">
        <option value="all">All Categories</option>
        {categories.map(cat => (
          <option key={cat} value={cat}>
            {cat.charAt(0).toUpperCase() + cat.slice(1)}
          </option>
        ))}
      </select>
      {(filterType !== "all" || filterCategory !== "all") && (
        <button
          className="btn-clear"
          onClick={() => {
            setFilterType("all");
            setFilterCategory("all");
            onFilterChange({ type: "all", category: "all" });
          }}
        >
          Clear Filters
        </button>
      )}
    </div>
  );
}