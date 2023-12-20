from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import PlaceOrderMedicineOne,OrderMedicineItem,MedicineStockList,PlacedOrderItems,ReceiveOrderItems,ItemUnitInventory,PlacedOrderMedicine,ReceiveOrderMedicine,MedicinePotencyStock

@receiver(m2m_changed, sender=PlaceOrderMedicineOne.vendor_order.through)
def handle_m2m_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add':
        # print(instance,instance.id,instance.vendor_order.all())
        queryset = MedicineStockList.objects.all()
        for q in queryset:
            if q.order_status == False:
                q.order_status = True
                q.save()
        placed_orders = PlaceOrderMedicineOne.objects.filter(id=instance.id)
        for p in placed_orders:
            for i in p.vendor_order.all():
                print("vendor",p,i)
                order_item = OrderMedicineItem.objects.create(vendor=i,ordered_med=p)
        # added_authors = Author.objects.filter(pk__in=pk_set)
        # print(f"Authors added to book '{instance}': {', '.join(str(author) for author in added_authors)}")

@receiver(m2m_changed, sender=PlacedOrderItems.vendors.through)
def handle_m2m_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add':
        queryset = ItemUnitInventory.objects.all()
        for q in queryset:
            if q.is_order_able == False:
                q.is_order_able = True
                q.save()
        orders = PlacedOrderItems.objects.filter(id=instance.id)
        for order in orders:
            for vendor in order.vendors.all():
                ReceiveOrderItems.objects.create(vendor=vendor,order=order)

@receiver(m2m_changed, sender=PlacedOrderMedicine.vendors.through)
def handle_m2m_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_add':
        queryset = MedicinePotencyStock.objects.all()
        for q in queryset:
            if q.is_order_able == False:
                q.is_order_able = True
                q.save()
        orders = PlacedOrderMedicine.objects.filter(id=instance.id)
        for order in orders:
            for vendor in order.vendors.all():
                ReceiveOrderMedicine.objects.create(vendor=vendor,order=order)