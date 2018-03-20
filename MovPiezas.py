#Ricardo Torres Sánchez A01334302
#Luis Villegas A01335257
def moverPeonB(indice,coordDestino):
    global enpassantB
    global columnaEnpassantB
    global indiceEnpassantB
    global enpassantN
    mover=0
    indiceContrario=99
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
        if vueltas != 0 or casillaOcupada:
            accion='invalido'
            
    elif accion=='comer':
        for cont in range(0,16):
            if posNegras[cont] == coordDestino:
                casillaOcupada=True
                break
        if casillaOcupada:
            indiceContrario=cont
##            mover=coordDestino
##            #Accion motor pasos
##            posBlancas[indice]=coordDestino
##            posNegras[cont]=posNegrasMorts[cont]
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
    return accion,indiceContrario

def moverPeonN(indice,coordDestino):
    global enpassantN
    global columnaEnpassantN
    global indiceEnpassantN
    global enpassantB
    mover=0
    indiceContrario=99
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
        if vueltas != 0 or casillaOcupada:
            accion='invalido'
            
    elif accion=='comer':
        for cont in range(0,16):
            if posBlancas[cont] == coordDestino:
                casillaOcupada=True
                break
        if casillaOcupada:
            indiceContrario=cont
##            mover=coordDestino
##            #Accion motor pasos
##            posNegras[indice]=coordDestino
##            posBlancas[cont]=posBlancasMorts[cont]
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
    return accion,indiceContrario

def moverPeon(indice,coordDestino,turnoBlancas):
    if turnoBlancas:
        accion,indiceCont=moverPeonB(indice,coordDestino)
    else:
        accion,indiceCont=moverPeonN(indice,coordDestino)
    return accion,indiceCont

def moverTorre(indice,coordDestino,turnoBlancas):
    global enpassantB
    global enpassantN
    mover=0
    signo=1
    indiceContrario=99
    if turnoBlancas:
        coordOrigen=posBlancas[indice]
    else:
        coordOrigen=posNegras[indice]

    casillaOcupada=False
    
    if coordDestino==coordOrigen:
        accion='invalido'
        #print(accion)
        return accion,indiceContrario
    elif (coordDestino&0xF0) - (coordOrigen&0xF0) == 0:
        accion='moverVertical'
        vueltas = (coordDestino&0xF) - (coordOrigen&0xF)
    elif (coordDestino&0xF) - (coordOrigen&0xF) == 0:
        accion='moverHorizontal'
        vueltas = (coordDestino&0xF0) - (coordOrigen&0xF0)
    else:
        accion='invalido'
        #print(accion)
        enpassantB=False
        enpassantN=False
        return accion,indiceContrario
    if vueltas<0:
        signo=-1
    
    if accion=='moverVertical':
        while vueltas != 0:
            vueltas = vueltas - 1*signo
            for cont in range(0,16):
                if posBlancas[cont] == coordDestino - vueltas:
                    if vueltas == 0 and not(turnoBlancas):
                        accion='comer'
                        break
                    else:
                        casillaOcupada=True
                        break
                if posNegras[cont] == coordDestino - vueltas:
                    if vueltas == 0 and turnoBlancas:
                        accion='comer'
                        break
                    else:
                        casillaOcupada=True
                        break
            if casillaOcupada:
                break
        if vueltas == 0 and not(casillaOcupada) and accion=='moverVertical':
            accion='mover'
##            mover=coordDestino
##            if turnoBlancas:
##                posBlancas[indice]=coordDestino
##            else:
##                posNegras[indice]=coordDestino
            ##Accion motor pasos
        elif accion=='comer':
            indiceContrario=cont
##            if turnoBlancas:
##                posBlancas[indice]=coordDestino
##                posNegras[cont]=posNegrasMorts[cont]
##            else:
##                posNegras[indice]=coordDestino
##                posBlancas[cont]=posBlancasMorts[cont]
        else:
            accion='invalido'
    elif accion=='moverHorizontal':
        while vueltas != 0:
            vueltas = vueltas - 0x10*signo
            for cont in range(0,16):
                if posBlancas[cont] == coordDestino - vueltas:
                    if vueltas == 0 and not(turnoBlancas):
                        accion='comer'
                        break
                    else:
                        casillaOcupada=True
                        break
                if posNegras[cont] == coordDestino - vueltas:
                    if vueltas == 0 and turnoBlancas:
                        accion='comer'
                        break
                    else:
                        casillaOcupada=True
                        break
            if casillaOcupada:
                break
        if vueltas == 0 and not(casillaOcupada) and accion=='moverHorizontal':
            accion='mover'
##            mover=coordDestino
##            if turnoBlancas:
##                posBlancas[indice]=coordDestino
##            else:
##                posNegras[indice]=coordDestino
            ##Accion motor pasos
        elif accion=='comer':
            indiceContrario=cont
##            if turnoBlancas:
##                posBlancas[indice]=coordDestino
##                posNegras[cont]=posNegrasMorts[cont]
##            else:
##                posNegras[indice]=coordDestino
##                posBlancas[cont]=posBlancasMorts[cont]
        else:
            accion='invalido'
    #print(accion)
    enpassantB=False
    enpassantN=False
    return accion,indiceContrario

def moverAlfil(indice,coordDestino,turnoBlancas):
    global enpassantB
    global enpassantN
    mover=0
    indiceContrario=99
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
                        break
                    else:
                        casillaOcupada=True
                        break
                if posNegras[cont] == coordDestino - difFilas - difColumnas:
                    if difFilas == 0 and turnoBlancas:
                        accion='comer'
                        break
                    else:
                        casillaOcupada=True
                        break
            if casillaOcupada:
                break
        if accion=='comer':
            indiceContrario=cont
        elif difFilas != 0 or casillaOcupada:
            accion='invalido'
    else:
        #print(accion)
        enpassantB=False
        enpassantN=False
        return accion,indiceContrario
    #print(accion)
    enpassantB=False
    enpassantN=False
    return accion,indiceContrario
        
def moverCaballo(indice, coordDestino, turnoBlancas):
    global enpassantB
    global enpassantN
    mover=0
    indiceContrario=99
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
        indiceContrario=cont

    #print(accion)
    enpassantB=False
    enpassantN=False
    return accion,indiceContrario

def moverReina(indice, coordDestino, turnoBlancas):
    indiceContrario=99
    if turnoBlancas:
        coordOrigen=posBlancas[indice]
    else:
        coordOrigen=posNegras[indice]
    
    difFilas=(coordDestino&0xF) - (coordOrigen&0xF)
    difColumnas=(coordDestino&0xF0) - (coordOrigen&0xF0)
    
    if difFilas==0 or difColumnas==0:
        accion,indiceContrario=moverTorre(indice, coordDestino, turnoBlancas)
    elif abs(difFilas)*0x10==abs(difColumnas):
        accion,indiceContrario=moverAlfil(indice, coordDestino, turnoBlancas)
    else:
        accion='invalido'
        #print(accion)
    return accion,indiceContrario

def moverRey(indice,coordDestino,turnoBlancas):
    indiceContrario=99
    if turnoBlancas:
        coordOrigen=posBlancas[indice]
    else:
        coordOrigen=posNegras[indice]
    
    difFilas=(coordDestino&0xF) - (coordOrigen&0xF)
    difColumnas=(coordDestino&0xF0) - (coordOrigen&0xF0)
    
    if abs(difFilas)==1 and abs(difColumnas)==0 or abs(difFilas)==0 and abs(difColumnas)==0x10:
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
        indiceContrario=cont

    #print(accion)
    enpassantB=False
    enpassantN=False
    return accion,indiceContrario

def funcionComer(indiceComedor,indiceComido,coordDestino,turnoBlancas):
    global jaqueN
    global jaqueB
    mover=coordDestino
    if indiceComido==15:
        accion='invalido'
    else:
        mover=coordDestino
        if turnoBlancas:
            coordOriginal=posBlancas[indiceComedor]
            posBlancas[indiceComedor]=coordDestino
            jaquePrevio=jaqueB
            jaqueB=checarJaqueB()
            if jaqueB:
                posBlancas[indiceComedor]=coordOriginal
                accion='invalido'
                jaqueB=jaquePrevio
            else:
                a=1
                accion='Sí se lo comió'
                posNegras[indiceComido]=posNegrasMorts[indiceComido]
                jaqueN=checarJaqueN()
                #Acción motor pasos
        else:
            coordOriginal=posNegras[indiceComedor]
            posNegras[indiceComedor]=coordDestino
            jaquePrevio=jaqueN
            jaqueN=checarJaqueN()
            if jaqueN:
                posNegras[indiceComedor]=coordOriginal
                accion='invalido'
                jaqueN=jaquePrevio
            else:
                a=1
                accion='Sí se lo comió'
                posBlancas[indiceComido]=posBlancasMorts[indiceComido]
                jaqueB=checarJaqueB()
                #Acción motor pasos
    return accion
        
def funcionMover(indice,coordDestino,turnoBlancas):
    global jaqueN
    global jaqueB
    mover=coordDestino
    if turnoBlancas:
        coordOriginal=posBlancas[indice]
        posBlancas[indice]=coordDestino
        jaquePrevio=jaqueB
        jaqueB=checarJaqueB()
        if jaqueB:
            posBlancas[indice]=coordOriginal
            accion='invalido'
            jaqueB=jaquePrevio
        else:
            a=1
            accion='Sí se movió'
            jaqueN=checarJaqueN()
            #Acción motor pasos
    else:
        coordOriginal=posNegras[indice]
        posNegras[indice]=coordDestino
        jaquePrevio=jaqueN
        jaqueN=checarJaqueN()
        if jaqueN:
            posNegras[indice]=coordOriginal
            accion='invalido'
            jaqueN=jaquePrevio
        else:
            a=1
            accion='Sí se movió'
            jaqueB=checarJaqueB()
            #Acción motor pasos
    return accion

def checarJaqueB():
    jaqueB=False
    for cont in range(0,15):
        if cont<8:
            accion,indiceC=moverPeon(cont,posBlancas[15],False)
            if accion=='comer':
                jaqueB=True
                break
        elif cont<10:
            accion,indiceC=moverTorre(cont,posBlancas[15],False)
            if accion=='comer':
                jaqueB=True
                break
        elif cont<12:
            accion,indiceC=moverCaballo(cont,posBlancas[15],False)
            if accion=='comer':
                jaqueB=True
                break
        elif cont<14:
            accion,indiceC=moverAlfil(cont,posBlancas[15],False)
            if accion=='comer':
                jaqueB=True
                break
        else:
            accion,indiceC=moverReina(cont,posBlancas[15],False)
            if accion=='comer':
                jaqueB=True
    return jaqueB

def checarJaqueN():
    jaqueN=False
    for cont in range(0,15):
        if cont<8:
            accion,indiceC=moverPeon(cont,posNegras[15],True)
            if accion=='comer':
                jaqueN=True
                break
        elif cont<10:
            accion,indiceC=moverTorre(cont,posNegras[15],True)
            if accion=='comer':
                jaqueN=True
                break
        elif cont<12:
            accion,indiceC=moverCaballo(cont,posNegras[15],True)
            if accion=='comer':
                jaqueN=True
                break
        elif cont<14:
            accion,indiceC=moverAlfil(cont,posNegras[15],True)
            if accion=='comer':
                jaqueN=True
                break
        else:
            accion,indiceC=moverReina(cont,posNegras[15],True)
            if accion=='comer':
                jaqueN=True
    return jaqueN

###########################################################################################################################3

posBlancas=[0x12,0x22,0x32,0x43,0x52,0x62,0x72,0x82,0x11,0x81,0x21,0x71,0x33,0x61,0x41,0x51]
posBlancasMorts=[0x01,0x02,0x03,0x04,0x94,0x93,0x92,0x91,0x10,0x80,0x20,0x70,0x30,0x60,0x40,0x50]

posNegras=[0x17,0x27,0x36,0x47,0x57,0x67,0x77,0x87,0x18,0x88,0x26,0x78,0x38,0x68,0x48,0x58]
posNegrasMorts=[0x08,0x07,0x06,0x05,0x95,0x96,0x97,0x98,0x19,0x89,0x29,0x79,0x39,0x69,0x49,0x59]

turnoBlancas=True
enpassantB=False
columnaEnpassantB=0
indiceEnpassantB=0
enpassantN=False
columnaEnpassantN=0
indiceEnpassantN=0

jaqueB=False
jaqueN=False

##accion,indiceContrario=moverPeon(2,0x34,turnoBlancas)
##print(accion)
##if accion=='mover':
##    accion=funcionMover(2,0x34,turnoBlancas)
##elif accion=='comer':
##    accion=funcionComer(2,indiceContrario,0x34,turnoBlancas)
##print(accion)
##
##turnoBlancas=False
##
##accion,indiceContrario=moverCaballo(10,0x34,turnoBlancas)
##print(accion)
##if accion=='mover':
##    accion=funcionMover(10,0x34,turnoBlancas)
##elif accion=='comer':
##    accion=funcionComer(10,indiceContrario,0x34,turnoBlancas)
##print(accion)
##
##turnoBlancas=True
##
##accion,indiceContrario=moverPeon(3,0x34,turnoBlancas)
##print(accion)
##if accion=='mover':
##    accion=funcionMover(3,0x34,turnoBlancas)
##elif accion=='comer':
##    accion=funcionComer(3,indiceContrario,0x34,turnoBlancas)
##print(accion)
##
##turnoBlancas=False
##
##accion,indiceContrario=moverReina(14,0x15,turnoBlancas)
##print(accion)
##if accion=='mover':
##    accion=funcionMover(14,0x15,turnoBlancas)
##elif accion=='comer':
##    accion=funcionComer(14,indiceContrario,0x15,turnoBlancas)
##print(accion)
##print(jaqueB)
##
##turnoBlancas=True
##
##accion,indiceContrario=moverPeon(1,0x24,turnoBlancas)
##print(accion)
##if accion=='mover':
##    accion=funcionMover(1,0x24,turnoBlancas)
##elif accion=='comer':
##    accion=funcionComer(1,indiceContrario,0x24,turnoBlancas)
##print(accion)
##print(jaqueB)
##
##accion,indiceContrario=moverPeon(1,0x25,turnoBlancas)
##print(accion)
##if accion=='mover':
##    accion=funcionMover(1,0x25,turnoBlancas)
##elif accion=='comer':
##    accion=funcionComer(1,indiceContrario,0x25,turnoBlancas)
##print(accion)
##print(jaqueB)
##
##turnoBlancas=False
##
##accion,indiceContrario=moverReina(14,0x24,turnoBlancas)
##print(accion)
##if accion=='mover':
##    accion=funcionMover(14,0x24,turnoBlancas)
##elif accion=='comer':
##    accion=funcionComer(14,indiceContrario,0x24,turnoBlancas)
##print(accion)
##print(jaqueB)
##
##turnoBlancas=True
##
##accion,indiceContrario=moverReina(14,0x42,turnoBlancas)
##print(accion)
##if accion=='mover':
##    accion=funcionMover(14,0x42,turnoBlancas)
##elif accion=='comer':
##    accion=funcionComer(14,indiceContrario,0x42,turnoBlancas)
##print(accion)
##print(jaqueB)
##
##accion,indiceContrario=moverReina(14,0x47,turnoBlancas)
##print(accion)
##if accion=='mover':
##    accion=funcionMover(14,0x47,turnoBlancas)
##elif accion=='comer':
##    accion=funcionComer(14,indiceContrario,0x47,turnoBlancas)
##print(accion)
##print(jaqueB)
##print(jaqueN)