export function Header () {
  return (
    <header className={styles.header}>
      <div className={styles.brand}>
        <NavLink to='/'>
          <img />
        </NavLink>
        <h1><NavLink to='/'>Runtime</NavLink></h1>
      </div>
      <nav>
        <ul>
          <li>
            <NavLink to='/configuraciones'>
              <img />
            </NavLink>
          </li>
        </ul>
      </nav>
    </header>
  )
}