@echo off
chcp 65001 > nul
cls
echo ===============================================================================
echo   LANZADOR DEL ENTORNO DE EJECUCION DE CODIGO MAQUINA (ACTIVIDAD 13)
echo   MATERIA: TRADUCTORES DE LENGUAJE / COMPILADORES
echo   PROFESOR: RIGOBERTO CARDENAS LARIOS
echo.
echo   INTEGRANTES DEL EQUIPO (ORDEN ALFABETICO POR PRIMER APELLIDO):
echo     1. DIAZ TORRES JAZMIN MONTSERRAT
echo     2. FIERRO MELENDEZ ERNESTO HATUEY
echo     3. HERNANDEZ GARCIA HECTOR GABRIEL
echo     4. MILLAN GUERRERO OSWALDO JOSUE
echo ===============================================================================
echo.

if "%~1"=="" (
    echo [USO]: run_program.bat ^<ruta_archivo_ejecutable.bin^>
    echo.
    echo No se especifico ningun archivo binario. Ejecutando caso_01 por defecto...
    echo.
    python -c "from virtual_machine import VirtualMachine; vm = VirtualMachine(); vm.load_executable_file('ejecutables/caso_01_mapeo_instrucciones.bin'); vm.run(); print('\n--- RESULTADOS EN MEMORIA RAM ---'); print(vm.dump_memory_state()); print('\n--- REGISTROS ---'); print(vm.dump_registers_state())"
) else (
    echo Cargando y ejecutando archivo binario: %1
    echo.
    python -c "import sys; from virtual_machine import VirtualMachine; vm = VirtualMachine(); vm.load_executable_file(sys.argv[1]); vm.run(); print('\n--- RESULTADOS EN MEMORIA RAM ---'); print(vm.dump_memory_state()); print('\n--- REGISTROS ---'); print(vm.dump_registers_state())" "%~1"
)

echo.
echo ===============================================================================
echo   EJECUCION FINALIZADA
echo ===============================================================================
pause

