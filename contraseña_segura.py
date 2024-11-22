def contraseñaSegura(contraseña):

    if contraseña.len() >= 8:
        return True

    if [] in contraseña:
        return True
    
    return False
