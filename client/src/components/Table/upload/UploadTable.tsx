interface Props {
    fileInfo: {
        name: string,
        size: number,
        type: string,
    }
}

const UploadTable = ({ fileInfo }: Props) => {
    
    const  { name, size } = fileInfo;

    return (
        <div className='model-table'>
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th className="col-md-2" scope="col">File name</th>
                        <th className="col-md-2" scope="col">Size</th>
                        
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>{name}</td>
                        {/* Adding thousand separators */}
                        <td>{`${Math.round(size / 1024).toLocaleString('en-UK')} kB`}</td> 
                    </tr>
                </tbody>
            </table>
        </div>
    );
}

export default UploadTable;