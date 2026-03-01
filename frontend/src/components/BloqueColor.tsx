import { useColorStore } from '../store/colorStore'

export default function BloqueColor({
  className,
  children,
  id,
  colorDefault,
}: {
  className: string
  children: React.ReactNode
  id: number
  colorDefault: string
}) {
  const color = useColorStore(state => state.colores[id] || colorDefault)
  return (
    <article
      className={className}
      style={
        {
          borderLeftColor: `${color}95`,
          '--color': color,
        } as React.CSSProperties
      }
    >
      {children}
    </article>
  )
}