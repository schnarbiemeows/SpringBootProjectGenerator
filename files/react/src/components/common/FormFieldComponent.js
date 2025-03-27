export default function FormFieldComponent({ field, objectName, handleChange, handleBlur, errors, touched }) {
    return (
        <div className="form-group">
            <label>{field.label}</label>
            <input
                type={field.type}
                className="form-control"
                name={field.name}
                value={objectName[field.name] || ""}
                onChange={handleChange}
                onBlur={handleBlur}
                placeholder={field.placeholder}
                pattern={field.pattern || undefined} // Only add pattern if it exists
            />
            {errors[field.name] && touched[field.name] && (
                <div className="alert alert-danger">{errors[field.name]}</div>
            )}
        </div>
    )
}
