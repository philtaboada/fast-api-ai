class SunatInfo:
    def __init__(
            self, numero_de_ruc, 
            tipo_contribuyente, 
            tipo_de_documento, 
            nombre_comercial, 
            fecha_de_inscripcion, 
            fecha_de_inicio_de_actividades,
            estado_del_contribuyente, 
            condicion_del_contribuyente,
            domicilio_fiscal,
            sistema_emision_de_comprobante,
            actividad_comercio_exterior,
            sistema_contabilidad,
            actividades_economicas,
            comprobantes_de_pago_cu_impresos,
            sistema_de_emision_electronica,
            emisor_electronico_desde,
            comprobantes_electronicos,
            afiliado_al_ple_desde,
            padrones
            ):
        
        self.numero_de_ruc = numero_de_ruc
        self.tipo_contribuyente = tipo_contribuyente
        self.tipo_de_documento = tipo_de_documento
        self.nombre_comercial = nombre_comercial
        self.fecha_de_inscripcion = fecha_de_inscripcion
        self.fecha_de_inicio_de_actividades = fecha_de_inicio_de_actividades
        self.estado_del_contribuyente = estado_del_contribuyente
        self.condicion_del_contribuyente = condicion_del_contribuyente
        self.domicilio_fiscal = domicilio_fiscal
        self.sistema_emision_de_comprobante = sistema_emision_de_comprobante
        self.actividad_comercio_exterior = actividad_comercio_exterior
        self.sistema_contabilidad = sistema_contabilidad
        self.actividades_economicas = actividades_economicas
        self.comprobantes_de_pago_cu_impresos = comprobantes_de_pago_cu_impresos
        self.sistema_de_emision_electronica = sistema_de_emision_electronica
        self.emisor_electronico_desde = emisor_electronico_desde
        self.comprobantes_electronicos = comprobantes_electronicos
        self.afiliado_al_ple_desde = afiliado_al_ple_desde
        self.padrones = padrones

    def __str__(self):
        return (f"SunatInfo(numero_de_ruc='{self.numero_de_ruc}', "
                f"tipo_contribuyente='{self.tipo_contribuyente}', "
                f"tipo_de_documento='{self.tipo_de_documento}', "
                f"nombre_comercial='{self.nombre_comercial}', "
                f"fecha_de_inscripcion='{self.fecha_de_inscripcion}', "
                f"fecha_de_inicio_de_actividades='{self.fecha_de_inicio_de_actividades}', "
                f"estado_del_contribuyente='{self.estado_del_contribuyente}', "
                f"condicion_del_contribuyente='{self.condicion_del_contribuyente}', "
                f"domicilio_fiscal='{self.domicilio_fiscal}', "
                f"sistema_emision_de_comprobante='{self.sistema_emision_de_comprobante}', "
                f"actividad_comercio_exterior='{self.actividad_comercio_exterior}', "
                f"sistema_contabilidad='{self.sistema_contabilidad}', "
                f"actividades_economicas='{self.actividades_economicas}', "
                f"comprobantes_de_pago_cu_impresos='{self.comprobantes_de_pago_cu_impresos}', "
                f"sistema_de_emision_electronica='{self.sistema_de_emision_electronica}', "
                f"emisor_electronico_desde='{self.emisor_electronico_desde}', "
                f"comprobantes_electronicos='{self.comprobantes_electronicos}', "
                f"afiliado_al_ple_desde='{self.afiliado_al_ple_desde}', "
                f"padrones='{self.padrones}', ")
    


