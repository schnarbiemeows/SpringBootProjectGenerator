import ButtonComponent from "./ButtonComponent";
import FormFieldComponent from "./FormFieldComponent";

export default function FormComponent({ className, addMode , editMode , objectName , setObject,
                                          validateField, saveResults, onCancel, errors,
                                          touched, setTouched, fieldsConfig}) {
    const isFormValid = () => {
        return (
            Object.values(errors).every(error => error === "") &&
            Object.values(touched).some(field => field)
        )
    }
    const handleSubmit = (event) => {
        event.preventDefault()
    }
    const handleChange = (e) => {
        setObject({
            ...objectName,  // Keep existing values
            [e.target.name]: e.target.value,  // Update only the changed field
        })
        validateField(e,e.target.name,e.target.value)
    }

    const handleBlur = (e) => {
        setTouched({ ...touched, [e.target.name]: true })
    }

    return (
        <div className="card card-body mb-3">
            {addMode && <h2>Add {className}...</h2>}
            {editMode && <h2>Edit {className}...</h2>}
            <form onSubmit={($event) => handleSubmit($event)}>
                {fieldsConfig.map(field => (
                    <FormFieldComponent
                        key={field.name}
                        field={field}
                        objectName={objectName}
                        handleChange={handleChange}
                        handleBlur={handleBlur}
                        errors={errors}
                        touched={touched}
                    />
                ))}
                {
                    (addMode || editMode) && <ButtonComponent message={"Save"} callFunction={saveResults}
                                                           color={"btn-success"} disabled={!isFormValid}/>
                }
                {(addMode || editMode) && <ButtonComponent message={"Cancel"} callFunction={onCancel}
                                                           color={"btn-danger"} disabled={!isFormValid}/>}
            </form>
        </div>
    )
}
