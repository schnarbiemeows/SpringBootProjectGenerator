import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faEdit, faTrash} from "@fortawesome/free-solid-svg-icons";

export default function ListItemComponent({ dto, i, fields, addMode, editMode,
                                              editItem, deleteItem }) {
    return (
        <tr className="a" key={i}>
            {fields.map(({key,value}) => {
                return (
                    <th key={key}>
                        <i className="text-size-6">{dto[key]}</i>
                    </th>
                )
            })}
            <td>
                <button className="btn-edit" type="submit" disabled={addMode || editMode}
                        onClick={() => editItem(i)}>
                    <FontAwesomeIcon  icon={faEdit} style={{color: "red"}}>

                    </FontAwesomeIcon>
                </button>
            </td>
            <td>
                <button className="btn-edit" type="submit" disabled={addMode || editMode}
                        onClick={() => deleteItem(i)}>
                    <FontAwesomeIcon icon={faTrash} style={{color:"blue"}}>

                    </FontAwesomeIcon>
                </button>
            </td>
        </tr>
    )
}
