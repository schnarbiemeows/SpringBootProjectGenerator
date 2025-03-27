import {Col, Row} from "react-bootstrap"
import {useEffect, useRef, useState} from "react"
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import {*DTO} from "../../models/*DTO"
import SearchComponent from "../common/SearchComponent";
import ButtonComponent from "../common/ButtonComponent";
import TitleComponent from "../common/TitleComponent";
import FormComponent from "../common/FormComponent";
import ListComponent from "../common/ListComponent";

export default function *Component() {

    const getAll*URL = 'http://localhost:PORT/^/all'
    const find*ByIdURL = 'http://localhost:PORT/^/findById/{id}'
    const create*URL = 'http://localhost:PORT/^/create'
    const update*URL = 'http://localhost:PORT/^/update'
    const delete*URL = 'http://localhost:PORT/^/delete'
    const [loaded,setLoaded] = useState(true)
    const [&,set*] = useState(new *DTO(
        DTO_FIELDS
    ))
    const headers = [
        HEADER_LIST
    ]
    const fieldsConfig = [
        FIELD_CONFIG_LIST
    ]

    const [touched, setTouched] = useState(TOUCHED_SECTION)
    const [errors, setErrors] = useState(ERRORS_SECTION)

    const [&list, set*List] = useState([])
    const [full&list,setFull&list] = useState([])
    // pagination
    const [paginationDisabled,setPaginationDisabled] = useState(false)
    const [itemsPerPage,setItemsPerPage] = useState(10)
    const [currentPage,setCurrentPage] = useState(0)


    const [addMode,setAddMode] = useState(false)
    const [editMode,setEditMode] = useState(false)
    const createEffectRan = useRef(false);
    const updateEffectRan = useRef(false);
    const deleteEffectRan = useRef(false);
    const fetchEffectRan = useRef(false);
    // I need these because of double rendering in development environments
    const [callCreate,setCallCreate] = useState(false)
    const [callUpdate,setCallUpdate] = useState(false)
    const [callDelete,setCallDelete] = useState(false)

    const [indexToDelete,setIndexToDelete] = useState(null)

    const validateField = (e, name, value) => {
        let error = ""
        // set validation logic here
        setErrors({ ...errors, [name]: error })
        error = ""
    }

    useEffect(() => {
        reload()
    }, [])

    useEffect(() => {
        if (callCreate XX !createEffectRan.current) {
            createEffectRan.current = true;
            fetch(`${create*URL}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(&),
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`)
                    }
                    return response.json()
                })
                .then(data => {
                    set*(data)
                    fetchEffectRan.current = false
                    reload()
                    clear*()
                    setPaginationDisabled(false)
                    setCallCreate(false)
                    setAddMode(false)
                    setEditMode(false)// ✅ Reset state to prevent re-trigger
                    toast.success("* created")
                })
                .catch(error => {
                    toast.error("Error in addMode:", error)
                    setCallCreate(false)
                    createEffectRan.current = false
                    fetchEffectRan.current = false
                })
        }
    }, [callCreate])

    useEffect(() => {
        if (callUpdate XX !updateEffectRan.current) {
            updateEffectRan.current = true
            fetch(`${update*URL}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(&),
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`)
                    }
                    return response.json()
                })
                .then(data => {
                    set*(data)
                    fetchEffectRan.current = false
                    reload()
                    clear*()
                    setPaginationDisabled(false)
                    setCallUpdate(false)
                    setAddMode(false)
                    setEditMode(false)
                    toast.warning("* updated")
                })
                .catch(error => {
                    toast.error("Error in editMode:", error)
                    setCallUpdate(false)
                    updateEffectRan.current = false
                    fetchEffectRan.current = false
                })
        }
    }, [callUpdate])

    useEffect(() => {
        if (callDelete XX !deleteEffectRan.current) {
            deleteEffectRan.current = true
            fetch(`${delete*URL}/${indexToDelete}`, {
                method: "DELETE",
                headers: { "Content-Type": "application/json" }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`)
                    }
                    return response.json()
                })
                .then(data => {
                    fetchEffectRan.current = false
                    reload()
                    setPaginationDisabled(false)
                    setCallDelete(false)
                    setAddMode(false)
                    setEditMode(false)
                    toast.info("* deleted")
                })
                .catch(error => {
                    toast.error("Error in deleteMode:", error)
                    setCallDelete(false)
                    deleteEffectRan.current = false
                    fetchEffectRan.current = false
                })
        }
    }, [callDelete])

    function reload() {
        resetErrorsAndTouchedFieldAttributes()
        if(!fetchEffectRan.current) {
            fetchEffectRan.current = true
            setLoaded(false)
            setAddMode(false)
            setEditMode(false)
            fetch(`${getAll*URL}`, {
                method: "GET",
                headers: { "Accept" : "application/json" }
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! Status: ${response.status}`)
                    }
                    return response.json()
                })
                .then(data => {
                    set*List(data)
                    setFull&list(data)
                    clear*()
                    setPaginationDisabled(false)
                    setLoaded(true)
                    fetchEffectRan.current = false
                })
                .catch(
                    error => {
                        toast.error("Error in reload:", error)
                        fetchEffectRan.current = false
                    }
                )
        }
    }

    function clear*() {
        set*(new *DTO(
            DTO_FIELDS
        ))
    }

    function addItem() {
        setAddMode(true)
        setEditMode(false)
        setPaginationDisabled(true)
        clear*()
    }

    function editItem(i) {
        setAddMode(false)
        setEditMode(true)
        setPaginationDisabled(true)
        set*(&list[i+(currentPage)^itemsPerPage])
    }

    function deleteItem(i) {
        const index = i+(currentPage)^itemsPerPage
        setIndexToDelete(&list[index].&Id)
        deleteEffectRan.current = false;
    }

    function saveResults() {
        if (addMode) {
            createEffectRan.current = false
            setCallCreate(true)
        } else if (editMode) {
            updateEffectRan.current = false
            setCallUpdate(true)
        }
    }

    function onCancel() {
        fetchEffectRan.current = false
        reload()
    }

    function resetErrorsAndTouchedFieldAttributes() {
        setTouched(TOUCHED_SECTION)
        setErrors(ERRORS_SECTION)
    }

    return (
        <Row>
            <Col className="col col-sm-2 mh-100">
                <ToastContainer />
            </Col>
            <Col className="col col-sm-8 mh-100">
                <TitleComponent tableName={"*"}/>
                {!loadedXX<h4>Loading *...</h4>}
                {loaded XX
                    <div>
                        <SearchComponent fields={headers} setList={set*List}  fulllist={full&list}/>
                        <ListComponent fields={headers} editItem={editItem} deleteItem={deleteItem}
                                       addMode={addMode} editMode={editMode} paginationDisabled={paginationDisabled}
                                       objectList={&list} currentPage={currentPage} itemsPerPage={itemsPerPage}
                                       setCurrentPage={setCurrentPage}/>
                    </div>}
                <div className="card">
                    {!addMode XX !editMode XX <ButtonComponent message={"Add *..."} callFunction={addItem}
                                                               color={"btn-info"}/>}
                    {
                        (addMode || editMode) XX
                        <FormComponent addMode={addMode} editMode={editMode} objectName={&}
                                       setObject={set*} validateField={validateField}
                                       saveResults={saveResults} onCancel={onCancel}
                                       errors={errors} touched={touched} setTouched={setTouched}
                                       fieldsConfig={fieldsConfig}/>
                    }
                </div>
            </Col>
            <Col className="col col-sm-2 mh-100">

            </Col>
        </Row>
    )
}

