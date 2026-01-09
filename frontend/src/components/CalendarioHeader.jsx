import styles from './CalendarioHeader.module.css'

function CalendarioTitle ({ date }) {
  const fecha = date
    .toLocaleDateString('es-ES', {
      month: 'long',
      year: 'numeric'
    })
    // El primer char a uppercase
    .replace(/^./, c => c.toUpperCase())
    .replace(/ de /g, ' ')
  return (
    <>
      <h2>{fecha}</h2>
      <p>Gestiona tus bloques de actividad diaria.</p>
    </>
  )
}

function CalendarioToolbar ({ prevDia, nextDia, irHoy }) {
  return (
    <>
      <div role='group' className={styles.viewBtn}>
        <button className='btn'>Mes</button>
        <button className='btn'>Semana</button>
      </div>
      <div className={styles.navBtn}>
        <button className='iconBtn' onClick={prevDia}>
          <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-outline icon-tabler-chevron-left'><path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M15 6l-6 6l6 6' /></svg>
        </button>
        <button className='btn' onClick={irHoy}>Hoy</button>
        <button className='iconBtn' onClick={nextDia}>
          <svg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='currentColor' strokeWidth='2' strokeLinecap='round' strokeLinejoin='round' className='icon icon-tabler icons-tabler-outline icon-tabler-chevron-right'><path stroke='none' d='M0 0h24v24H0z' fill='none' /><path d='M9 6l6 6l-6 6' /></svg>
        </button>
      </div>
    </>
  )
}

export default function CalendarioHeader ({ fecha, prevDia, nextDia, irHoy }) {
  return (
    <>
      <header className={styles.header}>
        <div className={styles.titleWrapper}>
          <CalendarioTitle date={fecha} />
        </div>
        <div className={styles.toolbarWrapper}>
          <CalendarioToolbar
            prevDia={prevDia}
            nextDia={nextDia}
            irHoy={irHoy}
          />
        </div>
      </header>
    </>
  )
}
