export default function SearchComponent({ fields, setList, fulllist }) {

    function isNullOrUndefined(input) {
        if(input === 'undefined') return true
        if(input == null) return true
        return false
    }

    function searchFunction(searchTerm) {
        let results = []
        for (const listItem of fulllist) {
            let include = false
            fields.map(({key}) => {
                if(!isNullOrUndefined(listItem[key])&&listItem[key].toString().toLowerCase().indexOf(searchTerm.toLowerCase()) !== -1){
                    console.log(key)
                    include = true
                }
            })
            if(include)
            {
                results.push(listItem)
            }
        }
        setList(results)
        if (results.length === 0 || !searchTerm) {
            setList(fulllist)
        }
    }


    return (
        <div className="card border-info">
            <form className="form-inline my-2 my-lg-0 justify-content-right">
                <input name="searchTerm" className="form-control mr-sm-2"
                       onChange={(e) => searchFunction(e.target.value)}
                       type="search" placeholder="Search records..."></input>
            </form>
        </div>
    )
}
