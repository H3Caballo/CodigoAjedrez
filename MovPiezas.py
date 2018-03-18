#Ricardo Torres Sánchez
def moverPeonB(indice,coordDestino):
    mover=0
    coordOrigen=posBlancas[indice]
    casillaOcupada=False
    if coordOrigen&0xF==2 and (coordDestino&0xF) - (coordOrigen&0xF) == 2 and (coordDestino&0xF0) - (coordOrigen&0xF0) == 0 : 
        accion='mover'
    elif (coordDestino&0xF) - (coordOrigen&0xF) == 1 :
        if (coordDestino&0xF0) - (coordOrigen&0xF0) == 0 :
            accion='mover'
        elif (coordDestino&0xF0) - (coordOrigen&0xF0) == 0x10 or (coordDestino&0xF0) - (coordOrigen&0xF0) == -0x10:
            accion='comer'
        else:
            accion='invalido'
    else:
        accion='invalido'
    
    vueltas = (coordDestino&0xF) - (coordOrigen&0xF)
    
    if accion=='mover':
        while vueltas > 0:
            vueltas -= 1
            for cont in range(0,16):
                if posBlancas[cont] == coordDestino - vueltas:
                    casillaOcupada=True
                    break
                if posNegras[cont] == coordDestino - vueltas:
                    casillaOcupada=True
                    break
            if casillaOcupada:
                break
        if vueltas == 0 and not(casillaOcupada):
            mover=coordDestino
            posBlancas[indice]=coordDestino
            ##Accion motor pasos
        else:
            accion='invalido'
    elif accion=='comer':
        for cont in range(0,15):
            if posNegras[cont] == coordDestino:
                casillaOcupada=True
                break
        if casillaOcupada:
            mover=coordDestino
            posBlancas[indice]=coordDestino
            posNegras[cont]=posNegrasMorts[cont]
        else:
            accion='invalido'
    print(accion)
    ##print(coordOrigen)
    ##print(cont)
    return

def moverTorre(indice,coordDestino,turnoBlancas):
    mover=0
    signo=1
    if turnoBlancas:
        coordOrigen=posBlancas[indice]
    else:
        coordOrigen=posNegras[indice]

    casillaOcupada=False
    
    if coordDestino==coordOrigen:
        accion='invalido'
        print(accion)
        return
    elif (coordDestino&0xF0) - (coordOrigen&0xF0) == 0:
        accion='moverVertical'
        vueltas = (coordDestino&0xF) - (coordOrigen&0xF)
    elif (coordDestino&0xF) - (coordOrigen&0xF) == 0:
        accion='moverHorizontal'
        vueltas = (coordDestino&0xF0) - (coordOrigen&0xF0)
    else:
        accion='invalido'
        print(accion)
        return
    if vueltas<0:
        signo=-1
    ##print(vueltas)
    ##print(accion)
    ##print(signo)
    
    if accion=='moverVertical':
        while vueltas != 0:
            vueltas = vueltas - 1*signo
            for cont in range(0,16):
                if posBlancas[cont] == coordDestino - vueltas:
                    if vueltas == 0 and not(turnoBlancas):
                        accion='comer'
                    else:
                        casillaOcupada=True
                        break
                if posNegras[cont] == coordDestino - vueltas:
                    if vueltas == 0 and turnoBlancas:
                        accion='comer'
                    else:
                        casillaOcupada=True
                        break
            if casillaOcupada:
                break
        if vueltas == 0 and not(casillaOcupada) and accion=='moverVertical':
            mover=coordDestino
            if turnoBlancas:
                posBlancas[indice]=coordDestino
            else:
                posNegras[indice]=coordDestino
            ##Accion motor pasos
        elif accion=='comer':
            if turnoBlancas:
                posBlancas[indice]=coordDestino
                posNegras[cont]=posNegrasMorts[cont]
            else:
                posNegras[indice]=coordDestino
                posBlancas[cont]=posBlancasMorts[cont]
        else:
            accion='invalido'
    elif accion=='moverHorizontal':
        while vueltas != 0:
            vueltas = vueltas - 0x10*signo
            for cont in range(0,16):
                if posBlancas[cont] == coordDestino - vueltas:
                    if vueltas == 0 and not(turnoBlancas):
                        accion='comer'
                    else:
                        casillaOcupada=True
                        break
                if posNegras[cont] == coordDestino - vueltas:
                    if vueltas == 0 and turnoBlancas:
                        accion='comer'
                    else:
                        casillaOcupada=True
                        break
            if casillaOcupada:
                break
        if vueltas == 0 and not(casillaOcupada) and accion=='moverHorizontal':
            mover=coordDestino
            if turnoBlancas:
                posBlancas[indice]=coordDestino
            else:
                posNegras[indice]=coordDestino
            ##Accion motor pasos
        elif accion=='comer':
            if turnoBlancas:
                posBlancas[indice]=coordDestino
                posNegras[cont]=posNegrasMorts[cont]
            else:
                posNegras[indice]=coordDestino
                posBlancas[cont]=posBlancasMorts[cont]
        else:
            accion='invalido'
    print(accion)
    return

def moverAlfil(indice,coordDestino,turnoBlancas):
    mover=0
    signoH=1
    signoV=1
    if turnoBlancas:
        coordOrigen=posBlancas[indice]
    else:
        coordOrigen=posNegras[indice]
    
    casillaOcupada=False
    difFilas=(coordDestino&0xF) - (coordOrigen&0xF)
    difColumnas=(coordDestino&0xF0) - (coordOrigen&0xF0)
    
    if coordDestino==coordOrigen:
        accion='invalido'
    elif abs(difFilas)*16 == abs(difColumnas):
        accion='mover'
        if difFilas<0:
            signoV=-1
        if difColumnas<0:
            signoH=-1
    else:
        accion='invalido'

    if accion=='mover':
        while difFilas != 0:
            difFilas = difFilas - 1*signoV
            difColumnas = difColumnas - 0x10*signoH
            for cont in range(0,16):
                if posBlancas[cont] == coordDestino - difFilas - difColumnas:
                    if difFilas == 0 and not(turnoBlancas):
                        accion='comer'
                    else:
                        casillaOcupada=True
                        break
                if posNegras[cont] == coordDestino - difFilas - difColumnas:
                    if difFilas == 0 and turnoBlancas:
                        accion='comer'
                    else:
                        casillaOcupada=True
                        break
            if casillaOcupada:
                break
        if difFilas == 0 and not(casillaOcupada) and accion=='mover':
            mover=coordDestino
            if turnoBlancas:
                posBlancas[indice]=coordDestino
            else:
                posNegras[indice]=coordDestino
            ##Accion motor pasos
        elif accion=='comer':
            if turnoBlancas:
                posBlancas[indice]=coordDestino
                posNegras[cont]=posNegrasMorts[cont]
            else:
                posNegras[indice]=coordDestino
                posBlancas[cont]=posBlancasMorts[cont]
        else:
            accion='invalido'
    else:
        print(accion)
        return
    print(accion)
    return
        
def moverCaballo(coordOrigen, coordDestino, turnoBlancas):
    mover=0
    casillaOcupada=False
    if (coordDestino&0xF) - (coordOrigen&0xF) == 2 and ((coordDestino&0xF0) - (coordOrigen&0xF0) == 0x10 or (coordDestino&0xF0) - (coordOrigen&0xF0) == -0x10):
        accion='moverAdelante'
    elif (coordDestino&0xF) - (coordOrigen&0xF) == -2 and ((coordDestino&0xF0) - (coordOrigen&0xF0) == 0x10 or (coordDestino&0xF0) - (coordOrigen&0xF0) == -0x10):
        accion='moverAtras'
    elif ((coordDestino&0xF) - (coordOrigen&0xF) == 1 or (coordDestino&0xF) - (coordOrigen&0xF) == -1) and (coordDestino&0xF0) - (coordOrigen&0xF0) == 0x20:
        accion='moverDerecha'
    elif ((coordDestino&0xF) - (coordOrigen&0xF) == 1 or (coordDestino&0xF) - (coordOrigen&0xF) == -1) and (coordDestino&0xF0) - (coordOrigen&0xF0) == -0x20:
        accion='moverIzquierda'
    else:
        accion='invalido'

    comer=0              ## casilla desocupada = 0 y casilla ocupada por pieza opuesta = 1
    if accion=='moverAdelante' or accion=='moverAtras' or accion=='moverDerecha' or accion=='moverIzquierda':
        if turnoBlancas==0:
            for cont in range(0,16):
                if posBlancas[cont] == coordDestino:
                    comer=0
                    casillaOcupada=True
                    break
                if posNegras[cont]-0x80 == coordDestino:
                    comer=1
                    casillaOcupada=True
                    break
            if comer==0:
                if casillaOcupada==True:
                    accion='invalido'
                    mover=coordDestino
                else:
                    accion='mover'
                    mover=coordDestino
            else:
                accion='comer'
                mover=coordDestino
        else:
            for cont in range(0,16):
                if posBlancas[cont] == coordDestino:
                    comer=1
                    casillaOcupada=True
                    break
                if posNegras[cont]-0x80 == coordDestino:
                    comer=0
                    casillaOcupada=True
                    break
            if comer==1:
                accion='mover'
                mover=coordDestino
            else:
                if casillaOcupada==True:
                    accion='invalido'
                    mover=coordDestino
                else:
                    accion='mover'
                    mover=coordDestino
    else:
        accion='invalido'

    print(accion)
    print(mover)
    return

posBlancas=[0x12,0x22,0x32,0x42,0x52,0x62,0x72,0x82,0x11,0x81,0x21,0x71,0x31,0x61,0x41,0x51]
posBlancasMorts=[0x01,0x02,0x03,0x04,0x94,0x93,0x92,0x91,0x10,0x80,0x20,0x70,0x30,0x60,0x40,0x50]

posNegras=[0x17,0x27,0x37,0x47,0x57,0x67,0x77,0x87,0x18,0x88,0x28,0x78,0x38,0x68,0x48,0x58]
posNegrasMorts=[0x08,0x07,0x06,0x05,0x95,0x96,0x97,0x98,0x19,0x89,0x29,0x79,0x39,0x69,0x49,0x59]

turnoBlancas=True
#moverTorre(8,0x18,turnoBlancas)
moverAlfil(12,0x35,turnoBlancas)
