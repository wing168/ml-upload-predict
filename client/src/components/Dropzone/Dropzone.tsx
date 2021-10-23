import { useCallback, Dispatch, SetStateAction } from 'react';
import { useDropzone } from 'react-dropzone';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCloudUploadAlt } from '@fortawesome/free-solid-svg-icons';

import './Dropzone.styles.css';

interface Props {
    setFileInfo: Dispatch<SetStateAction<{ name: string, size: number, type: string }>>,
    setFileData: Dispatch<SetStateAction<any>>,
}

const Dropzone = ({ setFileInfo, setFileData } : Props) => {

    const onDrop = useCallback((acceptedFiles) => {
        acceptedFiles.forEach((file: any) => {
            const reader = new FileReader();
            
            reader.onabort = () => console.log('file was aborted');
            reader.onerror = () => console.log('error with file');
            reader.onload = () => {

                setFileInfo(file);
                setFileData(reader.result);
            }
            reader.readAsArrayBuffer(file);
        });

    }, []);

    const { getRootProps, getInputProps } = useDropzone({ onDrop });

    return (
        <div className='drop-border' { ...getRootProps() }>
            <input { ...getInputProps() } />
            <h6 className='upload-text'>Drag and drop model file here</h6>
            <FontAwesomeIcon 
                className='upload-icon'
                icon={faCloudUploadAlt}
            />
            <h6 className='upload-text'>Or click to open file explorer</h6>
        </div>
    );
}

export default Dropzone;