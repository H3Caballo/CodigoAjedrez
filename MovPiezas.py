#Ricardo Torres Sánchez A01334302
#Luis Villegas A01335257
def moverPeonB(indice,coordDestino,enpassantN,columnaEnpassantN,indiceEnpassantN):
    mover=0
    enpassantB=False
    columnaEnpassantB=0
    indiceEnpassantB=0
    coordOrigen=posBlancas[indice]
    casillaOcupada=False
    if coordOrigen&0xF==2 and (coordDestino&0xF) - (coordOrigen&0xF) == 2 and (coordDestino&0xF0) - (coordOrigen&0xF0) == 0 : 
        accion='mover'
        enpassantB=True
        columnaEnpassantB=coordOrigen&0xF0
        indiceEnpassantB=indice
    elif (coordDestino&0xF) - (coordOrigen&0xF) == 1 :
        if (coordDestino&0xF0) - (coordOrigen&0xF0) == 0 :
            accion='mover'
        elif (coordDestino&0xF0) - (coordOrigen&0xF0) == 0x10 or (coordDestino&0xF0) - (coordOrigen&0xF0) == -0x10:
            #Una vez probando que funciona, probar con elif abs((coordDestino&0xF0) - (coordOrigen&0xF0)) == 0x10:
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
                enpassantB=False
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
            #Accion motor pasos
            posBlancas[indice]=coordDestino
            posNegras[cont]=posNegrasMorts[cont]
        elif enpassantN:
            if columnaEnpassantN == coordDestino&0xF0:
                mover=coordDestino
                #Accion motor pasos
                posBlancas[indice]=coordDestino
                posNegras[indiceEnpassantN]=posNegrasMorts[indiceEnpassantN]
        else:
            accion='invalido'
    #print(accion)
    enpassantN=False
    return accion,enpassantB,columnaEnpassantB,indiceEnpassantB

def moverPeonN(indice,coordDestino,enpassantB,columnaEnpassantB,indiceEnpassantB):
    mover=0
    enpassantN=False
    columnaEnpassantN=0
    indiceEnpassantN=0
    coordOrigen=posNegras[indice]
    casillaOcupada=False
    if coordOrigen&0xF==7 and (coordOrigen&0xF) - (coordDestino&0xF) == 2 and (coordDestino&0xF0) - (coordOrigen&0xF0) == 0 : 
        accion='mover'
        enpassantN=True
        columnaEnpassantN=coordOrigen&0xF0
        indiceEnpassantN=indice
    elif (coordOrigen&0xF) - (coordDestino&0xF) == 1 :
        if (coordDestino&0xF0) - (coordOrigen&0xF0) == 0 :
            accion='mover'
        elif (coordDestino&0xF0) - (coordOrigen&0xF0) == 0x10 or (coordDestino&0xF0) - (coordOrigen&0xF0) == -0x10:
            #Una vez probando que funciona, probar con elif abs((coordDestino&0xF0) - (coordOrigen&0xF0)) == 0x10:
            accion='comer'
        else:
            accion='invalido'
    else:
        accion='invalido'
    
    vueltas = (coordOrigen&0xF) - (coordDestino&0xF)
    
    if accion=='mover':
        while vueltas > 0:
            vueltas -= 1
            for cont in range(0,16):
                if posBlancas[cont] == coordDestino + vueltas:
                    casillaOcupada=True
                    break
                if posNegras[cont] == coordDestino + vueltas:
                    casillaOcupada=True
                    break
            if casillaOcupada:
                enpassantN=False
                break
        if vueltas == 0 and not(casillaOcupada):
            mover=coordDestino
            posNegras[indice]=coordDestino
            ##Accion motor pasos
        else:
            accion='invalido'
    elif accion=='comer':
        for cont in range(0,15):
            if posBlancas[cont] == coordDestino:
                casillaOcupada=True
                break
        if casillaOcupada:
            mover=coordDestino
            #Accion motor pasos
            posNegras[indice]=coordDestino
            posBlancas[cont]=posBlancasMorts[cont]
        elif enpassantB:
            if columnaEnpassantB == coordDestino&0xF0:
                mover=coordDestino
                #Accion motor pasos
                posNegras[indice]=coordDestino
                posBlancas[indiceEnpassantB]=posBlancasMorts[indiceEnpassantB]
        else:
            accion='invalido'
    #print(accion)
    enpassantB=False
    return accion,enpassantN,columnaEnpassantN,indiceEnpassantN

def moverPeon(indice,coordDestino,turnoBlancas,enpassantB,columnaEnpassantB,indiceEnpassantB,enpassantN,columnaEnpassantN,indiceEnpassantN):
    if turnoBlancas:
        accion=moverPeonB(indice,coordDestino,enpassantN,columnaEnpassantN,indiceEnpassantN)
    else:
        accion=moverPeonN(indice,coordDestino,enpassantB,columnaEnpassantB,indiceEnpassantB)
    return accion

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
        #print(accion)
        return accion
    elif (coordDestino&0xF0) - (coordOrigen&0xF0) == 0:
        accion='moverVertical'
        vueltas = (coordDestino&0xF) - (coordOrigen&0xF)
    elif (coordDestino&0xF) - (coordOrigen&0xF) == 0:
        accion='moverHorizontal'
        vueltas = (coordDestino&0xF0) - (coordOrigen&0xF0)
    else:
        accion='invalido'
        #print(accion)
        return accion
    if vueltas<0:
        signo=-1
    
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
    #print(accion)
    return accion

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
        #print(accion)
        return accion
    #print(accion)
    return accion
        
def moverCaballo(indice, coordDestino, turnoBlancas):
    mover=0
    if turnoBlancas:
        coordOrigen=posBlancas[indice]
    else:
        coordOrigen=posNegras[indice]

    casillaOcupada=False
    
    difFilas=(coordDestino&0xF) - (coordOrigen&0xF)
    difColumnas=(coordDestino&0xF0) - (coordOrigen&0xF0)
    
    if abs(difFilas) == 2 and abs(difColumnas) == 0x10 or abs(difFilas) == 1 and abs(difColumnas) == 0x20:
        accion='mover'
    else:
        accion='invalido'
        
    if accion=='mover':
        for cont in range(0,16):
            if posBlancas[cont] == coordDestino:
                if turnoBlancas:
                    accion='invalido'
                else:
                    accion='comer'
                break
            if posNegras[cont] == coordDestino:
                if not(turnoBlancas):
                    accion='invalido'
                else:
                    accion='comer'
                break
    if accion=='comer':
        if turnoBlancas:
            posBlancas[indice]=coordDestino
            posNegras[cont]=posNegrasMorts[cont]
        else:
            posNegras[indice]=coordDestino
            posBlancas[cont]=posBlancasMorts[cont]

    #print(accion)
    return accion

def moverReina(indice, coordDestino, turnoBlancas):
    if turnoBlancas:
        coordOrigen=posBlancas[indice]
    else:
        coordOrigen=posNegras[indice]
    
    difFilas=(coordDestino&0xF) - (coordOrigen&0xF)
    difColumnas=(coordDestino&0xF0) - (coordOrigen&0xF0)
    
    if difFilas==0 or difColumnas==0:
        accion=moverTorre(indice, coordDestino, turnoBlancas)
    elif abs(difFilas)*0x10==abs(difColumnas):
        accion=moverAlfil(indice, coordDestino, turnoBlancas)
    else:
        accion='invalido'
        #print(accion)
    return accion

posBlancas=[0x12,0x22,0x32,0x42,0x52,0x62,0x72,0x82,0x11,0x81,0x21,0x71,0x31,0x61,0x41,0x51]
posBlancasMorts=[0x01,0x02,0x03,0x04,0x94,0x93,0x92,0x91,0x10,0x80,0x20,0x70,0x30,0x60,0x40,0x50]

posNegras=[0x17,0x27,0x37,0x47,0x57,0x67,0x77,0x87,0x18,0x88,0x28,0x78,0x38,0x68,0x48,0x58]
posNegrasMorts=[0x08,0x07,0x06,0x05,0x95,0x96,0x97,0x98,0x19,0x89,0x29,0x79,0x39,0x69,0x49,0x59]

turnoBlancas=True
#accion=moverTorre(8,0x18,turnoBlancas)
#accion=moverAlfil(12,0x35,turnoBlancas)
#accion=moverReina(14,0x45,turnoBlancas)
enpassantB=False
columnaEnpassantB=0
indiceEnpassantB=0
enpassantN=False
columnaEnpassantN=0
indiceEnpassantN=0

accion,enpassantB,columnaEnpassantB,indiceEnpassantB=moverPeon(0,0x14,turnoBlancas,enpassantB,columnaEnpassantB,indiceEnpassantB,enpassantN,columnaEnpassantN,indiceEnpassantN)
turnoBlancas=False
accion,enpassantN,columnaEnpassantN,indiceEnpassantN=moverPeon(1,0x13,turnoBlancas,enpassantB,columnaEnpassantB,indiceEnpassantB,enpassantN,columnaEnpassantN,indiceEnpassantN)
print(accion)
