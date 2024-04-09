import React, { useState, useEffect } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { FileUpload } from 'primereact/fileupload';
import axios from 'axios'; // Asegúrate de instalar axios con `npm install axios`
import './TablaSalarios.css';

const TablaSalarios = () => {
    const [empleados, setEmpleados] = useState([]);

    useEffect(() => {
        // Obtener empleados al cargar el componente
        const obtenerEmpleados = async () => {
            try {
                const respuesta = await axios.get('http://localhost:5500/empleados');
                setEmpleados(respuesta.data);
            } catch (error) {
                console.error('Error al obtener los empleados:', error);
            }
        };

        obtenerEmpleados();
    }, []);

    const onUpload = async (e) => {
        const formData = new FormData();
        formData.append('file', e.files[0]);
    
        try {
            // Subir el archivo al servidor
            const response = await axios.post('http://localhost:5500/subir', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });
            
            // Si la subida fue exitosa, refrescar la lista de empleados
            if (response.status === 200) {
                await obtenerEmpleados(); // Esta llamada actualizará el estado `empleados`
            }
        } catch (error) {
            console.error('Error al subir el archivo:', error);
        }
    };
    
    // La función obtenerEmpleados se define fuera de useEffect para que pueda ser reutilizada
    const obtenerEmpleados = async () => {
        try {
            const respuesta = await axios.get('http://localhost:5500/empleados');
            setEmpleados(respuesta.data);
            console.log(respuesta.data); // Verificar los datos recibidos
        } catch (error) {
            console.error('Error al obtener los empleados:', error);
        }
    };
    

    return (
        <div className="tabla-salarios-container">
            <h1 className="titulo-sistema-nomina">Sistema de Nómina</h1>
            <FileUpload
                name="demo[]"
                customUpload
                uploadHandler={onUpload}
                accept=".csv"
                maxFileSize={1000000}
                className="upload-container"
            />
            
            <div className="card datatable-fullscreen">
                <DataTable value={empleados} responsiveLayout="scroll">
                    <Column field="nombre" header="Nombre"></Column>
                    <Column field="telefono" header="Teléfono"></Column>
                    <Column field="cargo" header="Cargo"></Column>
                    <Column field="horas_trabajo" header="Horas"></Column>
                    <Column field="salario" header="Salario"></Column>
                    <Column field="fecha_carga" header="Fecha"></Column>
                    <Column field="hora_carga" header="Hora"></Column>
                </DataTable>
            </div>
        </div>
    );
};

export default TablaSalarios;
