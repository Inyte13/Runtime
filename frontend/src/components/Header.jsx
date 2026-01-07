import { Link } from 'react-router'
export function Header () {
  return (
    <header className={styles.header}>
      <div className={styles.brand}>
        <Link to='/'>
          <img />
        </Link>
        <h1><Link to='/'>Runtime</Link></h1>
      </div>
      <nav>
        <ul>
          <li>
            <Link to='/configuraciones'>
              <img />
            </Link>
          </li>
        </ul>
      </nav>
    </header>
  )
}
