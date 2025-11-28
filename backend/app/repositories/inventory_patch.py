from sqlalchemy.dialects.postgresql import insert

def create_many(self, inventories):
    from app.models.inventory import Inventory
    
    for inventory in inventories:
        stmt = insert(Inventory).values(
            record_id=inventory.record_id,
            hospital_id=inventory.hospital_id,
            blood_group=inventory.blood_group.value,
            component=inventory.component.value,
            units=inventory.units,
            unit_expiry_date=inventory.unit_expiry_date,
            collection_date=inventory.collection_date
        ).on_conflict_do_update(
            index_elements=['record_id'],
            set_={
                'hospital_id': inventory.hospital_id,
                'blood_group': inventory.blood_group.value,
                'component': inventory.component.value,
                'units': inventory.units,
                'unit_expiry_date': inventory.unit_expiry_date,
                'collection_date': inventory.collection_date
            }
        )
        self.db.execute(stmt)
    
    self.db.commit()
    return []
