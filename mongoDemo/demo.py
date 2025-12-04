from pymongo import MongoClient,  read_concern, write_concern
from pymongo.errors import ConnectionFailure
from bson import ObjectId
from datetime import datetime, timedelta
import random

def connect_to_mongodb():
    """Conectar al replica set de MongoDB"""
    try:
        # Connection string para replica set
        client = MongoClient(
            "mongodb://localhost:27017,localhost:27018,localhost:27019/?replicaSet=rs0",
            serverSelectionTimeoutMS=5000
        )
        
        # Verificar conexión
        client.admin.command('ping')
        print("Conexión exitosa al replica set de MongoDB")
        
        # Verificar que hay un PRIMARY
        status = client.admin.command('replSetGetStatus')
        primary = [m for m in status['members'] if m['stateStr'] == 'PRIMARY']
        if primary:
            print(f"PRIMARY encontrado: {primary[0]['name']}")
        
        return client
        
    except ConnectionFailure as e:
        print(f"Error de conexión: {e}")
        print("Verifica que:")
        print("  1. Los contenedores estén corriendo: docker-compose ps")
        print("  2. El replica set esté inicializado: docker exec -it mongo1 mongosh --eval 'rs.status()'")
        exit(1)

# =============================================================================
# DATOS DE EJEMPLO
# =============================================================================

def get_sample_plans():
    """Catálogo de planes de suscripción"""
    return [
        {
            "plan_code": "plus_monthly_usd",
            "name": "Duolingo Plus Monthly",
            "tier": "plus",
            "billing_cycle": "monthly",
            "price": {
                "amount": 12.99,
                "currency": "USD"
            },
            "features": [
                "ad_free",
                "offline_mode",
                "unlimited_hearts",
                "progress_tracking"
            ],
            "trial_days": 7,
            "active": True,
            "available_countries": ["US", "CA", "UK", "AU", "UY"],
            "metadata": {
                "marketing_name": "Premium Monthly",
                "display_order": 1
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "schema_version": 1
        },
        {
            "plan_code": "plus_annual_usd",
            "name": "Duolingo Plus Annual",
            "tier": "plus",
            "billing_cycle": "annual",
            "price": {
                "amount": 83.88,
                "currency": "USD"
            },
            "features": [
                "ad_free",
                "offline_mode",
                "unlimited_hearts",
                "progress_tracking",
                "mastery_quizzes"
            ],
            "trial_days": 14,
            "active": True,
            "available_countries": ["US", "CA", "UK", "AU", "UY"],
            "metadata": {
                "marketing_name": "Premium Annual - Best Value!",
                "display_order": 2,
                "discount_vs_monthly": "35%"
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "schema_version": 1
        },
        {
            "plan_code": "family_annual_usd",
            "name": "Duolingo Family Annual",
            "tier": "family",
            "billing_cycle": "annual",
            "price": {
                "amount": 119.99,
                "currency": "USD"
            },
            "features": [
                "ad_free",
                "offline_mode",
                "unlimited_hearts",
                "progress_tracking",
                "mastery_quizzes",
                "family_sharing_6_members"
            ],
            "trial_days": 14,
            "active": True,
            "available_countries": ["US", "CA", "UK", "AU"],
            "metadata": {
                "marketing_name": "Family Plan - Up to 6 Members",
                "display_order": 3,
                "max_members": 6
            },
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "schema_version": 1
        }
    ]

def get_sample_coupons():
    """Cupones promocionales"""
    now = datetime.utcnow()
    return [
        {
            "code": "NEWYEAR2025",
            "type": "percentage",
            "value": 25,
            "currency": "USD",
            "applies_to": {
                "type": "all",
                "plan_ids": []
            },
            "restrictions": {
                "max_redemptions": 10000,
                "redemptions_count": 3247,
                "max_per_user": 1,
                "min_purchase": 50.00,
                "new_users_only": False
            },
            "validity": {
                "start": datetime(2025, 1, 1),
                "end": datetime(2025, 1, 31, 23, 59, 59)
            },
            "active": True,
            "created_at": datetime(2024, 12, 15),
            "updated_at": now,
            "schema_version": 1
        },
        {
            "code": "STUDENT50",
            "type": "percentage",
            "value": 50,
            "currency": "USD",
            "applies_to": {
                "type": "specific_plans",
                "plan_ids": []  # Se llenarán después
            },
            "restrictions": {
                "max_redemptions": 5000,
                "redemptions_count": 892,
                "max_per_user": 1,
                "min_purchase": 0,
                "new_users_only": True
            },
            "validity": {
                "start": now - timedelta(days=30),
                "end": now + timedelta(days=335)
            },
            "active": True,
            "created_at": now - timedelta(days=30),
            "updated_at": now,
            "schema_version": 1
        }
    ]

def generate_sample_users(count=20):
    """Generar usuarios de ejemplo"""
    first_names = ["Ana", "Carlos", "María", "Juan", "Laura", "Diego", "Sofia", "Miguel", 
                   "Elena", "Pablo", "Carmen", "Luis", "Isabel", "Fernando", "Valentina",
                   "Andrés", "Lucía", "Ricardo", "Daniela", "Roberto"]
    last_names = ["García", "Rodríguez", "Martínez", "López", "González", "Pérez", "Sánchez",
                  "Ramírez", "Torres", "Flores", "Rivera", "Gómez", "Díaz", "Cruz", "Morales"]
    
    users = []
    for i in range(count):
        first = random.choice(first_names)
        last = random.choice(last_names)
        email = f"{first.lower()}.{last.lower()}{random.randint(1,999)}@example.com"
        
        users.append({
            "_id": ObjectId(),
            "email": email,
            "username": f"{first.lower()}{random.randint(100,999)}",
            "full_name": f"{first} {last}",
            "created_at": datetime.utcnow() - timedelta(days=random.randint(30, 730)),
            "country": random.choice(["US", "UY", "AR", "MX", "ES", "CA"])
        })
    
    return users

# =============================================================================
# CARGA DE DATOS
# =============================================================================

def load_sample_data(db):
    """Cargar datos de ejemplo en la base de datos"""
    
    print("\n" + "="*60)
    print("CARGANDO DATOS DE EJEMPLO")
    print("="*60)
    
    # 1. PLANES
    print("\nInsertando planes...")
    plans_collection = db.plans
    plans_collection.drop()  # Limpiar colección
    
    plans = get_sample_plans()
    result = plans_collection.insert_many(plans)
    plan_ids = result.inserted_ids
    print(f"{len(plan_ids)} planes insertados")
    
    # Mostrar planes
    for plan in plans:
        print(f"   - {plan['name']}: ${plan['price']['amount']} {plan['price']['currency']}")
    
    # 2. CUPONES
    print("\n Insertando cupones...")
    coupons_collection = db.coupons
    coupons_collection.drop()
    
    coupons = get_sample_coupons()
    # Asignar plan_ids al cupón STUDENT50
    coupons[1]['applies_to']['plan_ids'] = [plan_ids[0], plan_ids[1]]  # Monthly y Annual
    
    result = coupons_collection.insert_many(coupons)
    coupon_ids = result.inserted_ids
    print(f"{len(coupon_ids)} cupones insertados")
    
    for coupon in coupons:
        print(f"   - {coupon['code']}: {coupon['value']}% off")
    
    # 3. USUARIOS
    print("\nGenerando usuarios...")
    users = generate_sample_users(20)
    print(f"{len(users)} usuarios generados")
    
    # 4. SUSCRIPCIONES
    print("\nCreando suscripciones...")
    subscriptions_collection = db.subscriptions
    subscriptions_collection.drop()
    
    subscriptions = []
    statuses = ["active", "active", "active", "active", "past_due", "canceled", "paused"]
    
    for i, user in enumerate(users[:15]):  # 15 de 20 usuarios tienen suscripción
        plan = random.choice(plans)
        status = random.choice(statuses)
        
        # Calcular fechas según el billing cycle
        if plan['billing_cycle'] == 'monthly':
            period_days = 30
        else:
            period_days = 365
        
        start_date = datetime.utcnow() - timedelta(days=random.randint(0, 60))
        end_date = start_date + timedelta(days=period_days)
        
        subscription = {
            "_id": ObjectId(),
            "user_id": user["_id"],
            "username": user["username"],
            "plan": {
                "plan_id": plan_ids[plans.index(plan)],
                "name": plan["name"],
                "tier": plan["tier"],
                "billing_cycle": plan["billing_cycle"],
                "price": plan["price"]
            },
            "status": status,
            "current_period": {
                "start": start_date,
                "end": end_date
            },
            "entitlements": [
                {
                    "feature": feature,
                    "enabled": status == "active",
                    "granted_at": start_date
                }
                for feature in plan["features"]
            ],
            "auto_renew": status in ["active", "past_due"],
            "cancel_at_period_end": status == "canceled",
            "canceled_at": start_date + timedelta(days=10) if status == "canceled" else None,
            "trial": {
                "is_trial": i < 3,  # Primeros 3 en trial
                "trial_end": start_date + timedelta(days=plan['trial_days']) if i < 3 else None
            },
            "payment_method": {
                "type": "credit_card",
                "psp_token": f"tok_visa_{random.randint(1000,9999)}",
                "last4": f"{random.randint(1000,9999)}",
                "brand": random.choice(["visa", "mastercard", "amex"]),
                "exp_month": random.randint(1, 12),
                "exp_year": random.randint(2025, 2028)
            },
            "metadata": {
                "acquisition_channel": random.choice(["mobile_app", "web", "referral"]),
                "promo_code_used": "NEWYEAR2025" if i % 4 == 0 else None
            },
            "created_at": start_date,
            "updated_at": datetime.utcnow(),
            "schema_version": 2
        }
        
        subscriptions.append(subscription)
    
    result = subscriptions_collection.insert_many(subscriptions)
    subscription_ids = result.inserted_ids
    print(f"{len(subscription_ids)} suscripciones insertadas")
    
    # Estadísticas de suscripciones
    status_counts = {}
    for sub in subscriptions:
        status_counts[sub['status']] = status_counts.get(sub['status'], 0) + 1
    
    print("\n   Estado de suscripciones:")
    for status, count in status_counts.items():
        print(f"   - {status}: {count}")
    
    # 5. FACTURAS
    print("\nGenerando facturas...")
    invoices_collection = db.invoices
    invoices_collection.drop()
    
    invoices = []
    invoice_counter = 1000
    
    for subscription in subscriptions:
        # Cada suscripción activa/pasada tiene 1-3 facturas
        num_invoices = random.randint(1, 3) if subscription['status'] in ['active', 'past_due', 'canceled'] else 1
        
        for inv_num in range(num_invoices):
            invoice_date = subscription['created_at'] + timedelta(days=inv_num * 30)
            
            # Determinar estado de la factura
            if subscription['status'] == 'active':
                invoice_status = random.choice(['paid', 'paid', 'paid', 'open'])
            elif subscription['status'] == 'past_due':
                invoice_status = random.choice(['open', 'uncollectible'])
            else:
                invoice_status = 'paid'
            
            subtotal = subscription['plan']['price']['amount']
            tax = round(subtotal * 0.08, 2)  # 8% tax
            total = subtotal + tax
            
            # Crear cargo
            charge_status = 'succeeded' if invoice_status == 'paid' else 'pending' if invoice_status == 'open' else 'failed'
            
            charge = {
                "charge_id": f"ch_{random.randint(10000,99999)}",
                "psp": "stripe",
                "amount": total,
                "status": charge_status,
                "payment_method": subscription['payment_method'],
                "failure_code": None if charge_status != 'failed' else random.choice(['card_declined', 'insufficient_funds']),
                "failure_message": None if charge_status != 'failed' else "Your card was declined.",
                "idempotency_key": f"idem_{subscription['user_id']}_{invoice_date.strftime('%Y%m%d')}_{total}",
                "psp_response": {
                    "transaction_id": f"txn_{random.randint(100000,999999)}",
                    "authorization_code": f"{random.randint(100000,999999)}" if charge_status == 'succeeded' else None
                },
                "created_at": invoice_date,
                "captured_at": invoice_date + timedelta(seconds=random.randint(1, 10)) if charge_status == 'succeeded' else None
            }
            
            invoice = {
                "_id": ObjectId(),
                "invoice_number": f"INV-2025-{invoice_counter:06d}",
                "user_id": subscription['user_id'],
                "username": subscription['username'],
                "subscription_id": subscription['_id'],
                "status": invoice_status,
                "subtotal": subtotal,
                "tax": tax,
                "total": total,
                "currency": "USD",
                "line_items": [
                    {
                        "description": subscription['plan']['name'],
                        "quantity": 1,
                        "unit_price": subtotal,
                        "amount": subtotal
                    }
                ],
                "coupon_redemptions": [],
                "charges": [charge],
                "refunds": [],
                "period": subscription['current_period'],
                "due_date": invoice_date,
                "paid_at": invoice_date + timedelta(seconds=5) if invoice_status == 'paid' else None,
                "created_at": invoice_date,
                "updated_at": datetime.utcnow(),
                "schema_version": 2
            }
            
            # Agregar cupón al 25% de las facturas
            if random.random() < 0.25:
                discount = round(subtotal * 0.25, 2)  # 25% off
                invoice['coupon_redemptions'] = [{
                    "coupon_id": coupon_ids[0],
                    "code": "NEWYEAR2025",
                    "discount_amount": discount,
                    "applied_at": invoice_date
                }]
                invoice['total'] = round(subtotal - discount + tax, 2)
                invoice['charges'][0]['amount'] = invoice['total']
            
            # Agregar reembolso al 10% de las facturas pagadas
            if invoice_status == 'paid' and random.random() < 0.1:
                refund_amount = round(total * 0.5, 2)  # Reembolso parcial
                invoice['refunds'] = [{
                    "refund_id": f"re_{random.randint(10000,99999)}",
                    "charge_id": charge['charge_id'],
                    "amount": refund_amount,
                    "reason": random.choice(["customer_request", "duplicate", "fraudulent"]),
                    "status": "succeeded",
                    "psp_response": {
                        "refund_transaction_id": f"ref_{random.randint(100000,999999)}"
                    },
                    "created_at": invoice_date + timedelta(days=random.randint(1, 10)),
                    "processed_at": invoice_date + timedelta(days=random.randint(1, 10), seconds=5)
                }]
            
            invoices.append(invoice)
            invoice_counter += 1
    
    result = invoices_collection.insert_many(invoices)
    print(f"{len(result.inserted_ids)} facturas insertadas")
    
    # Estadísticas de facturas
    invoice_status_counts = {}
    total_revenue = 0
    for inv in invoices:
        invoice_status_counts[inv['status']] = invoice_status_counts.get(inv['status'], 0) + 1
        if inv['status'] == 'paid':
            total_revenue += inv['total']
    
    print("\n   Estado de facturas:")
    for status, count in invoice_status_counts.items():
        print(f"   - {status}: {count}")
    print(f"\n Revenue total: ${total_revenue:.2f}")
    
    # 6. EVENTOS PSP (webhooks simulados)
    print("\nInsertando eventos PSP...")
    psp_events_collection = db.psp_events
    psp_events_collection.drop()
    
    psp_events = []
    for invoice in invoices[:10]:  # Solo primeros 10 para ejemplo
        for charge in invoice['charges']:
            event = {
                "_id": ObjectId(),
                "event_id": f"evt_stripe_{random.randint(100000,999999)}",
                "psp": "stripe",
                "type": f"charge.{charge['status']}",
                "payload": {
                    "charge_id": charge['charge_id'],
                    "amount": charge['amount'],
                    "status": charge['status']
                },
                "related_entities": {
                    "user_id": invoice['user_id'],
                    "subscription_id": invoice['subscription_id'],
                    "invoice_id": invoice['_id']
                },
                "processing": {
                    "status": "processed",
                    "attempts": 1,
                    "last_attempt_at": charge['created_at'] + timedelta(seconds=2),
                    "error_message": None
                },
                "idempotency_key": f"evt_stripe_{charge['charge_id']}",
                "received_at": charge['created_at'] + timedelta(seconds=1),
                "processed_at": charge['created_at'] + timedelta(seconds=2),
                "expires_at": charge['created_at'] + timedelta(days=90),
                "schema_version": 1
            }
            psp_events.append(event)
    
    result = psp_events_collection.insert_many(psp_events)
    print(f"✅ {len(result.inserted_ids)} eventos PSP insertados")
    
    print("\n" + "="*60)
    print("CARGA DE DATOS COMPLETADA")
    print("="*60)
    
    return {
        'users': users,
        'plans': plans,
        'plan_ids': plan_ids,
        'subscriptions': subscriptions,
        'subscription_ids': subscription_ids,
        'invoices': invoices,
        'coupons': coupons
    }

# =============================================================================
# EJEMPLO DE TRANSACCIÓN ACID
# =============================================================================

def ejemplo_transaccion_checkout(db, data):
    """
    Ejemplo de transacción ACID: Proceso de checkout
    
    Simula un usuario comprando una suscripción:
    1. Crear factura draft
    2. Verificar idempotencia
    3. Procesar cargo (simulado)
    4. Actualizar invoice a paid
    5. Activar/crear suscripción
    """
    
    print("\n" + "="*60)
    print("DEMOSTRACIÓN DE TRANSACCIÓN ACID - CHECKOUT")
    print("="*60)
    
    # Seleccionar un usuario sin suscripción
    existing_user_ids = [sub['user_id'] for sub in data['subscriptions']]
    available_users = [u for u in data['users'] if u['_id'] not in existing_user_ids]
    
    if not available_users:
        print("No hay usuarios sin suscripción, usando usuario existente")
        user = data['users'][0]
    else:
        user = available_users[0]
    
    # Seleccionar plan
    plan_id = data['plan_ids'][1]  # Plan anual
    plan = data['plans'][1]
    
    print(f"\nUsuario: {user['username']} ({user['email']})")
    print(f"Plan: {plan['name']} - ${plan['price']['amount']}")
    
    # Simular datos de checkout
    idempotency_key = f"idem_checkout_{user['_id']}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    payment_token = f"tok_test_{random.randint(1000,9999)}"
    
    print(f"\nIdempotency Key: {idempotency_key}")
    print(f"Payment Token: {payment_token}")
    
    # Iniciar sesión de transacción
    client = db.client
    
    print("\nIniciando transacción multi-documento...")
    
    with client.start_session() as session:
        try:
            # Iniciar transacción con snapshot isolation y write concern majority
            session.start_transaction(
                    read_concern=read_concern.ReadConcern(level='snapshot'),
                    write_concern=write_concern.WriteConcern(w='majority')
            )
            
            print("   ✓ Transacción iniciada (snapshot isolation, write concern majority)")
            
            # PASO 1: Verificar idempotencia (prevenir doble cargo)
            print("\n   [1/5] Verificando idempotencia...")
            existing_invoice = db.invoices.find_one(
                {"charges.idempotency_key": idempotency_key},
                session=session
            )
            
            if existing_invoice:
                print(f"  Operación duplicada detectada! Invoice existente: {existing_invoice['invoice_number']}")
                session.abort_transaction()
                return {"status": "duplicate", "invoice": existing_invoice}
            
            print("   ✓ No hay duplicados, continuando...")
            
            # PASO 2: Crear factura draft
            print("\n   [2/5] Creando factura draft...")
            
            subtotal = plan['price']['amount']
            tax = round(subtotal * 0.08, 2)
            total = round(subtotal + tax, 2)
            
            now = datetime.utcnow()
            invoice_doc = {
                "_id": ObjectId(),
                "invoice_number": f"INV-2025-{random.randint(900000,999999)}",
                "user_id": user['_id'],
                "username": user['username'],
                "subscription_id": None,  # Se actualizará después
                "status": "draft",
                "subtotal": subtotal,
                "tax": tax,
                "total": total,
                "currency": "USD",
                "line_items": [{
                    "description": plan['name'],
                    "quantity": 1,
                    "unit_price": subtotal,
                    "amount": subtotal
                }],
                "coupon_redemptions": [],
                "charges": [],
                "refunds": [],
                "period": {
                    "start": now,
                    "end": now + timedelta(days=365)
                },
                "due_date": now,
                "paid_at": None,
                "created_at": now,
                "updated_at": now,
                "schema_version": 2
            }
            
            result = db.invoices.insert_one(invoice_doc, session=session)
            invoice_id = result.inserted_id
            
            print(f"   ✓ Factura draft creada: {invoice_doc['invoice_number']}")
            print(f"      - Subtotal: ${subtotal}")
            print(f"      - Tax: ${tax}")
            print(f"      - Total: ${total}")
            
            # PASO 3: Simular llamada a PSP (en producción sería síncrona al procesador de pagos)
            print("\n   [3/5] Procesando cargo con PSP (simulado)...")
            import time
            time.sleep(1)  # Simular latencia de red
            
            charge_success = random.random() < 0.95
            
            if not charge_success:
                print("   Cargo rechazado por el PSP!")
                session.abort_transaction()
                return {"status": "payment_failed", "reason": "card_declined"}
            
            charge_result = {
                "charge_id": f"ch_{random.randint(100000,999999)}",
                "transaction_id": f"txn_{random.randint(100000,999999)}",
                "authorization_code": f"{random.randint(100000,999999)}",
                "status": "succeeded"
            }
            
            print(f"   ✓ Cargo exitoso!")
            print(f"      - Charge ID: {charge_result['charge_id']}")
            print(f"      - Transaction ID: {charge_result['transaction_id']}")
            
            # PASO 4: Actualizar invoice con cargo exitoso
            print("\n   [4/5] Actualizando factura con resultado del cargo...")
            
            charge_doc = {
                "charge_id": charge_result['charge_id'],
                "psp": "stripe",
                "amount": total,
                "status": "succeeded",
                "payment_method": {
                    "type": "credit_card",
                    "last4": payment_token[-4:],
                    "brand": "visa"
                },
                "failure_code": None,
                "failure_message": None,
                "idempotency_key": idempotency_key,
                "psp_response": {
                    "transaction_id": charge_result['transaction_id'],
                    "authorization_code": charge_result['authorization_code']
                },
                "created_at": now,
                "captured_at": datetime.utcnow()
            }
            
            db.invoices.update_one(
                {"_id": invoice_id},
                {
                    "$set": {
                        "status": "paid",
                        "paid_at": datetime.utcnow(),
                        "updated_at": datetime.utcnow()
                    },
                    "$push": {"charges": charge_doc}
                },
                session=session
            )
            
            print(f"   ✓ Factura actualizada a 'paid'")
            
            # PASO 5: Activar/crear suscripción
            print("\n   [5/5] Activando suscripción...")
            
            subscription_doc = {
                "user_id": user['_id'],
                "username": user['username'],
                "plan": {
                    "plan_id": plan_id,
                    "name": plan['name'],
                    "tier": plan['tier'],
                    "billing_cycle": plan['billing_cycle'],
                    "price": plan['price']
                },
                "status": "active",
                "current_period": {
                    "start": now,
                    "end": now + timedelta(days=365)
                },
                "entitlements": [
                    {
                        "feature": feature,
                        "enabled": True,
                        "granted_at": now
                    }
                    for feature in plan['features']
                ],
                "auto_renew": True,
                "cancel_at_period_end": False,
                "canceled_at": None,
                "trial": {
                    "is_trial": False,
                    "trial_end": None
                },
                "payment_method": {
                    "type": "credit_card",
                    "psp_token": payment_token,
                    "last4": payment_token[-4:],
                    "brand": "visa",
                    "exp_month": 12,
                    "exp_year": 2026
                },
                "metadata": {
                    "acquisition_channel": "web",
                    "promo_code_used": None
                },
                "created_at": now,
                "updated_at": now,
                "schema_version": 2
            }
            
            result = db.subscriptions.insert_one(subscription_doc, session=session)
            subscription_id = result.inserted_id
            
            print(f"   Suscripción creada y activada")
            print(f"      - Subscription ID: {subscription_id}")
            print(f"      - Status: active")
            print(f"      - Entitlements: {len(subscription_doc['entitlements'])} features")
            
            # Actualizar invoice con subscription_id
            db.invoices.update_one(
                {"_id": invoice_id},
                {"$set": {"subscription_id": subscription_id}},
                session=session
            )
            
            # COMMIT: Todo o nada
            print("\n   Haciendo commit de la transacción...")
            session.commit_transaction()
            print("   COMMIT EXITOSO - Todos los cambios persistidos atómicamente")
            
            print("\n" + "="*60)
            print("CHECKOUT COMPLETADO EXITOSAMENTE")
            print("="*60)
            print(f"\nResumen:")
            print(f"  - Invoice: {invoice_doc['invoice_number']}")
            print(f"  - Monto: ${total}")
            print(f"  - Suscripción: {subscription_id}")
            print(f"  - Usuario ahora tiene acceso premium ✨")
            
            return {
                "status": "success",
                "invoice_id": invoice_id,
                "invoice_number": invoice_doc['invoice_number'],
                "subscription_id": subscription_id,
                "amount": total
            }
            
        except Exception as e:
            print(f"\n   ERROR: {e}")
            print("   Haciendo ABORT de la transacción...")
            session.abort_transaction()
            print("   ✓ ABORT exitoso - Ningún cambio fue persistido")
            
            print("\n" + "="*60)
            print("CHECKOUT FALLIDO - Base de datos sin cambios")
            print("="*60)
            
            raise

# =============================================================================
# EJEMPLO DE TRANSACCIÓN: REEMBOLSO
# =============================================================================

def ejemplo_transaccion_reembolso(db, data):
    """
    Ejemplo de transacción ACID: Procesar reembolso
    
    1. Verificar que la factura existe y está paid
    2. Simular reembolso con PSP
    3. Registrar reembolso en invoice
    4. Si es reembolso total, cancelar suscripción
    """
    
    print("\n" + "="*60)
    print("DEMOSTRACIÓN DE TRANSACCIÓN ACID - REEMBOLSO")
    print("="*60)
    
    # Buscar una factura pagada
    paid_invoice = db.invoices.find_one({"status": "paid", "refunds": {"$size": 0}})
    
    if not paid_invoice:
        print(" No hay facturas pagadas sin reembolsos")
        return
    
    print(f"\nInvoice: {paid_invoice['invoice_number']}")
    print(f"Total: ${paid_invoice['total']}")
    print(f"User ID: {paid_invoice['user_id']}")
    
    # Reembolso total
    refund_amount = paid_invoice['total']
    is_full_refund = True
    
    print(f"\nProcesando reembolso total de ${refund_amount}...")
    
    client = db.client
    
    with client.start_session() as session:
        try:
            session.start_transaction(
                read_concern=read_concern.ReadConcern(level='snapshot'),
                write_concern=write_concern.WriteConcern(w='majority'),
            )
            
            print("   ✓ Transacción iniciada")
            
            # PASO 1: Simular reembolso con PSP
            print("\n   [1/3] Procesando reembolso con PSP...")
            import time
            time.sleep(0.5)
            
            refund_result = {
                "refund_id": f"re_{random.randint(100000,999999)}",
                "transaction_id": f"ref_{random.randint(100000,999999)}",
                "status": "succeeded"
            }
            
            print(f"   ✓ Reembolso exitoso: {refund_result['refund_id']}")
            
            # PASO 2: Registrar reembolso en invoice
            print("\n   [2/3] Registrando reembolso en factura...")
            
            refund_doc = {
                "refund_id": refund_result['refund_id'],
                "charge_id": paid_invoice['charges'][0]['charge_id'],
                "amount": refund_amount,
                "reason": "customer_request",
                "status": "succeeded",
                "psp_response": {
                    "refund_transaction_id": refund_result['transaction_id']
                },
                "created_at": datetime.utcnow(),
                "processed_at": datetime.utcnow()
            }
            
            db.invoices.update_one(
                {"_id": paid_invoice['_id']},
                {
                    "$push": {"refunds": refund_doc},
                    "$set": {"updated_at": datetime.utcnow()}
                },
                session=session
            )
            
            print(f"   ✓ Reembolso registrado")
            
            # PASO 3: Si es reembolso total, cancelar suscripción
            if is_full_refund and paid_invoice.get('subscription_id'):
                print("\n   [3/3] Cancelando suscripción (reembolso total)...")
                
                db.subscriptions.update_one(
                    {"_id": paid_invoice['subscription_id']},
                    {
                        "$set": {
                            "status": "canceled",
                            "canceled_at": datetime.utcnow(),
                            "entitlements": [],  # Revocar inmediatamente
                            "updated_at": datetime.utcnow()
                        }
                    },
                    session=session
                )
                
                print(f"   ✓ Suscripción cancelada y entitlements revocados")
            
            # COMMIT
            print("\n   💾 Haciendo commit...")
            session.commit_transaction()
            print("   ✅ COMMIT EXITOSO")
            
            print("\n" + "="*60)
            print("REEMBOLSO COMPLETADO")
            print("="*60)
            print(f"\nResumen:")
            print(f"  - Reembolso: ${refund_amount}")
            print(f"  - Invoice: {paid_invoice['invoice_number']}")
            print(f"  - Suscripción: {'Cancelada' if is_full_refund else 'Activa'}")
            
        except Exception as e:
            print(f"\n   ERROR: {e}")
            session.abort_transaction()
            print("   ✓ ABORT exitoso")
            raise

# =============================================================================
# QUERIES DE EJEMPLO
# =============================================================================

def ejemplos_queries(db):
    """Queries útiles para la demo"""
    
    print("\n" + "="*60)
    print("EJEMPLOS DE QUERIES")
    print("="*60)
    
    # 1. Suscripciones activas
    print("\n1. Contar suscripciones por estado:")
    pipeline = [
        {"$group": {"_id": "$status", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    results = list(db.subscriptions.aggregate(pipeline))
    for r in results:
        print(f"   - {r['_id']}: {r['count']}")
    
    # 2. Revenue total
    print("\n2. Revenue total (facturas pagadas):")
    pipeline = [
        {"$match": {"status": "paid"}},
        {"$group": {"_id": None, "total": {"$sum": "$total"}, "count": {"$sum": 1}}}
    ]
    result = list(db.invoices.aggregate(pipeline))
    if result:
        print(f"   - Total facturas: {result[0]['count']}")
        print(f"   - Revenue: ${result[0]['total']:.2f}")
    
    # 3. Usuarios con premium activo
    print("\n3. Usuarios con premium activo:")
    count = db.subscriptions.count_documents({"status": "active"})
    print(f"   - {count} suscripciones activas")
    
    # 4. Suscripciones próximas a renovar
    print("\n4. Suscripciones que renuevan en los próximos 7 días:")
    from_date = datetime.utcnow()
    to_date = from_date + timedelta(days=7)
    
    upcoming = db.subscriptions.count_documents({
        "status": "active",
        "auto_renew": True,
        "current_period.end": {"$gte": from_date, "$lte": to_date}
    })
    print(f"   - {upcoming} suscripciones")
    
    # 5. Plan más popular
    print("\n5. Planes más populares:")
    pipeline = [
        {"$match": {"status": {"$in": ["active", "past_due"]}}},
        {"$group": {"_id": "$plan.name", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 3}
    ]
    results = list(db.subscriptions.aggregate(pipeline))
    for i, r in enumerate(results, 1):
        print(f"   {i}. {r['_id']}: {r['count']} suscripciones")
    
    # 6. Tasa de fallo de pagos
    print("\n 6. Tasa de fallo de pagos:")
    total_charges = db.invoices.aggregate([
        {"$unwind": "$charges"},
        {"$group": {"_id": "$charges.status", "count": {"$sum": 1}}}
    ])
    for r in total_charges:
        print(f"   - {r['_id']}: {r['count']}")

def main():
    """Función principal"""
    
    print("""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   OBLIGATORIO BDDNR - TIENDA VIRTUAL Y SUSCRIPCIONES          ║
║   Script de Carga de Datos y Demo de Transacciones            ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Conectar
    client = connect_to_mongodb()
    db = client['duolingo']
    
    print(f"\nBase de datos: {db.name}")
    
    # Cargar datos de ejemplo
    data = load_sample_data(db)
    
    # Queries de ejemplo
    ejemplos_queries(db)
    
    # Ejemplos de transacciones
    input("\n⏸️  Presiona ENTER para ejecutar ejemplo de CHECKOUT (transacción)...")
    ejemplo_transaccion_checkout(db, data)
    
    input("\n⏸️  Presiona ENTER para ejecutar ejemplo de REEMBOLSO (transacción)...")
    ejemplo_transaccion_reembolso(db, data)
    
    # print("\n" + "="*60)
    # print("🎉 SCRIPT COMPLETADO")
    # print("="*60)
    # print("""
# Ahora puedes:
  # 1. Abrir Mongo Express: http://localhost:8081
  # 2. Abrir MongoDB Compass: mongodb://localhost:27017/?replicaSet=rs0
  # 3. Explorar las colecciones creadas
  # 4. Ejecutar tus propias queries
  
# Colecciones disponibles:
  # - plans (catálogo de productos)
  # - coupons (promociones)
  # - subscriptions (suscripciones activas/canceladas)
  # - invoices (facturas y cobros)
  # - psp_events (webhooks simulados)
    # """)

if __name__ == "__main__":
    # Instalar dependencias si no están:
    # pip install pymongo
    main()
