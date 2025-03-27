import ReactPaginate from "react-paginate";
import ListHeadComponent from "./ListHeadComponent";
import ListItemComponent from "./ListItemComponent";

export default function ListComponent({fields, editItem, deleteItem, addMode, editMode,
                                          paginationDisabled, objectList, currentPage, itemsPerPage,
                                          setCurrentPage}) {
    const currentList = paginationDisabled ? objectList :
        objectList.slice(currentPage*itemsPerPage, (currentPage+1)*itemsPerPage)
    const handlePageClick = ({ selected }) => {
        setCurrentPage(selected)
    }
    return (
        <div className="card border-info">
            <div className="card-body table-responsive">
                <table className="table-sm table-bordered table-hover rounded">
                    <ListHeadComponent fields={fields}/>
                    <tbody>
                    {currentList.map((dto, i) => (
                        <ListItemComponent dto={dto} i={i} fields={fields} addMode={addMode}
                        editMode={editMode} editItem={editItem} deleteItem={deleteItem}/>
                    ))}
                    </tbody>
                </table>
                <div className="card pagin">
                    {!paginationDisabled &&
                        <ReactPaginate
                            previousLabel={"← Previous"}
                            nextLabel={"Next →"}
                            breakLabel={"..."}
                            pageCount={Math.ceil(objectList.length / itemsPerPage)}
                            marginPagesDisplayed={2}
                            pageRangeDisplayed={3}
                            onPageChange={handlePageClick}
                            containerClassName={"pagination"}
                            activeClassName={"active"}
                        />
                    }
                </div>
            </div>
        </div>
    )
}
