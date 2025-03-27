export default function ListHeadComponent({ fields }) {
    return (
        <thead>
            <tr>
                {fields.map(({key,label}) => {
                    return (
                        <th key={key}>
                            <i className="text-size-10">{label}</i>
                        </th>
                    )
                })}
                <th>
                    <i className="text-size-8">Edit Item</i>
                </th>
                <th>
                    <i className="text-size-8">Delete Item</i>
                </th>
            </tr>
        </thead>
    )
}
