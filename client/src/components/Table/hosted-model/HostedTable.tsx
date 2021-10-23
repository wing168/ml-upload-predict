import './HostedTable.styles.css';

const HostedTable = () => {
    return (
        <div className='model-table'>
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Model name</th>
                        <th scope="col">URL</th>
                        <th scope="col">Size</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <th scope="row">1</th>
                        <td>XGBoost</td>
                        <td>https://ml-predict/XGboost-1</td>
                        <td>30,256 kB</td>
                    </tr>
                    <tr>
                        <th scope="row">2</th>
                        <td>CATBoost</td>
                        <td>https://ml-predict/CATboost-2</td>
                        <td>30,256 kB</td>
                    </tr>
                </tbody>
            </table>
        </div>
    )
}

export default HostedTable;