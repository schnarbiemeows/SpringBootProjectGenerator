export default function TitleComponent({ tableName }) {
    return (
        <div className="card bg-secondary border-info">
            <h2 className="text-center">{tableName}</h2>
        </div>
    )
}
