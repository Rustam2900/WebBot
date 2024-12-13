from django.db import models


class Vippacet(models.Model):
    image = models.ImageField(upload_to='static/vippacet/images', verbose_name="Paket Rasm")
    name = models.CharField(max_length=100, verbose_name="Paket Nomi")
    title = models.CharField(max_length=100, verbose_name="Paket Sarlavhasi")
    description = models.TextField(verbose_name="To'liq Tarif", help_text="Paket haqida batafsil ma'lumot.")
    price = models.DecimalField(max_digits=20, decimal_places=15, verbose_name="Umumiy Narx",
                                help_text="Paketning umumiy narxi.")
    duration = models.PositiveIntegerField(verbose_name="Davomiyligi (kun)",
                                           help_text="Paketning qancha davom etishi (kunlarda).")
    daily_price = models.DecimalField(max_digits=20, decimal_places=15, verbose_name="Kunlik Narx",
                                      help_text="Paket uchun kunlik narx.")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "VIP Paket"
        verbose_name_plural = "VIP Paketlar"
