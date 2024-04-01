const Todo = ({ title, description, completed, toggleCompleted, deleteTodo }) => {

  return (
    // Display Todo all on one line
    <>
      <h3>{title}</h3>
      <p>{description}</p>
      <input
        type="checkbox"
        checked={completed}
        onChange={() => toggleCompleted(title)}
      />
      <button onClick={() => deleteTodo(title)}>Delete</button>
    </>
  )
}

export default Todo