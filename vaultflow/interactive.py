from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from rich.console import Console
from .commands import initialize_vault, show_status, create_local_backup, push_changes_to_remote, start_experiment, finish_experiment, show_backups, show_vaults
from .config import is_managed_vault, get_managed_vaults

def _show_managed_vault_menu():
    """Muestra el menú de acciones para un vault gestionado."""
    console = Console()
    action_map = {
        "status": show_status,
        "backup": create_local_backup,
        "push": push_changes_to_remote,
        "backups": show_backups,
        "vaults": show_vaults,
    }

    while True:
        console.print("[magenta]" + "="*60 + "[/magenta]")
        choice = inquirer.select(
            message="¿Que te gustaria hacer?",
            choices=[
                Choice("status", name="Ver Estado del Vault"),
                Choice("backup", name="Crear Backup Local"),
                Choice("push", name="Sincronizar con Remoto (Push)"),
                Choice("backups", name="Ver Backups Disponibles"),
                Choice("vaults", name="Ver Todos los Vaults"),
                Choice("start_exp", name="Iniciar un Nuevo Experimento"),
                Choice("finish_exp", name="Finalizar un Experimento"),
                Choice(None, name="Salir")
            ],
            default="status"
        ).execute()

        if choice is None:
            print("¡Hasta luego!")
            break

        console.print("[magenta]" + "-"*60 + "[/magenta]")

        if choice in action_map:
            action_map[choice]()
        elif choice == "start_exp":
            exp_name = inquirer.text(message="Nombre del nuevo experimento:").execute()
            if exp_name: start_experiment(exp_name)
        elif choice == "finish_exp":
            exp_name = inquirer.text(message="Nombre del experimento a finalizar (sin 'exp/'):").execute()
            if exp_name: finish_experiment(exp_name)

def _show_unmanaged_vault_menu():
    """Muestra el menú de bienvenida/inicio para un directorio no gestionado."""
    console = Console()
    
    choices = [
        Choice("init", name="Iniciar vaultflow en este directorio"),
    ]
    
    registered_vaults = get_managed_vaults()
    for vault_path in registered_vaults:
        # Usamos el path como 'value' para saber a dónde ir
        choices.append(Choice(vault_path, name=f"Ir a vault existente: {vault_path}"))

    choices.append(Choice(None, name="Salir"))

    console.print("[yellow]Este directorio no esta gestionado por vaultflow.[/yellow]")
    selection = inquirer.select(
        message="Puedes:",
        choices=choices
    ).execute()

    if selection == "init":
        initialize_vault()
    elif selection is not None:
        # Cambiar al directorio seleccionado y lanzar el menú de vault gestionado
        import os
        try:
            os.chdir(selection)
            console.print(f"\n[green]✓ Navegando a: {selection}[/green]")
            console.print("[magenta]" + "="*60 + "[/magenta]")
            # Lanzar el menú de vault gestionado
            _show_managed_vault_menu()
        except (OSError, FileNotFoundError) as e:
            console.print(f"\n[red]✗ Error al cambiar al directorio: {e}[/red]")
            console.print("\nAccion recomendada:", style="bold yellow")
            console.print(f"cd \"{selection}\"")


def launch_interactive_menu():
    """
    Lanza el menú interactivo apropiado según el contexto del directorio.
    """
    # Mostramos un mensaje de bienvenida general una sola vez.
    print("\nBienvenido a vaultflow, una herramienta para gestionar tus vaults de Obsidian con Git.\n")

    if is_managed_vault():
        _show_managed_vault_menu()
    else:
        _show_unmanaged_vault_menu()