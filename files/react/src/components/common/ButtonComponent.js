export default function ButtonComponent({ message, callFunction, color, disabled=false }) {



    return (
        <button onClick={() => callFunction()}
         className={`btn btn-sm btn-block ${ color } text-white mb-3 font-italic`}
         disabled={disabled}>{ message }</button>
    )
}
