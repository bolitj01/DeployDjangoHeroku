const Todo = ({ title, description, completed, toggleCompleted, deleteTodo }) => {

  return (
    // Display Todo all on one line
    <>
      <h3 data-testid={`title-${title}`}>{title}</h3>
      <p data-testid={`description-${title}`}>{description}</p>
      <input
        data-testid={`completed-${title}`}
        type="checkbox"
        checked={completed}
        onChange={() => toggleCompleted(title)}
      />
      <button
        data-testid={`delete-${title}`}
        onClick={() => deleteTodo(title)}
      >Delete</button>
    </>
  )
}

export default Todo