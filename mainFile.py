
import smtplib, os,imaplib, getpass
import datetime , mailbox ,email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from tkinter.filedialog import askopenfile
from tkinter import Tk





# Mail gönderme İşlemlerimiz mailSend fonksiyonunda yapılmıştır.
def mailGonder():
    Tk().state("withdrawn")
            #maile ek eklemek için kullanılan fonksiyon.
    def attachment(file):
        attachment = MIMEBase('application', "octet-stream")
        attachment.set_payload(open(file,"rb").read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 'attachment; filename="%s"'%os.path.basename(file)) #kabaca işletim sistemimizde açılan pencerede seçtiğimiz dosyanın yolunu ve ismini bulmuş oluyoruz
        mail.attach(attachment) #bu kod bloğu ile de mesajımıza eklemiş olduk
        print("Attachment başarıyla mesajınıza eklendi.")

    kulllaniciGelen = ["hotmail","gmail"] #kullanıcının girdiği ifadeyi belirlemek için kurduğumuz döngü satırları ve değişken
    for option in kulllaniciGelen:
        print("{}) {}".format(kulllaniciGelen.index(option)+1, option))

    kullanıcıGiris = int(input("Kullanmak istediğiniz sırasını giriniz : "))

    kullaniciAdi = input("Kullanıcı adınız : ")
    kullaniciPass = input("Şifreniz : ")

    mail = MIMEMultipart()
    mesajBaslik = input("Mesajınızın Başlığı : ")
    mail.attach(MIMEText(input("Mesajınızı giriniz : "))) #Mailimize göndereceğimiz mesajımızı aldık
    mesajFrom = kullaniciAdi
    print("Mesajınızı birden fazla kişiye göndermek istiyorsanız :\nE-Mail adresleri arasına ',' koyunuz.")
    mesajKime = input("Kime : ") #mailin kime gideceğini belirttiğimiz kod blokları
    if "," in mesajKime:
        sendThem = mesajKime.split(",") # eğer araya , konulduysa mesaj birden fazla kişiye gidecek anlamına gelir ve , den önce ve sonrakiler alınır.
        recipients = [i.strip() for i in sendThem]
    else: recipients = [mesajKime]

    try: mesajTekrar = int(input("Kaç kez : ")) #Maili kaç defa göndermek istediğimizi belirttiğimiz ve gerçekleştirğimiz kod bloğu
    except: mesajTekrar = 1

    attachmentYesNo = input("Mesajınıza attachment eklemek için 'y' yazınız : ") #Mailimize ek eklemek isteyip istemediğimizi sorduğumuz kod bloğu
    if attachmentYesNo == "y":   #Mailimize ek eklemek için kullanının isteğine göre ekleme ifadesi
        attachmentAsk = askopenfile(title = "Attachment Seçiniz")
        attachmentPath = attachmentAsk.name
        attachment(attachmentPath)

    mail['Subject'] = mesajBaslik #Mail Başlığımız
    mail['From'] = mesajFrom #Maili kimden alacağımız
    mail['To'] = ", ".join(recipients)
    print("Bağlantı kuruluyor...")
    if kulllaniciGelen[kullanıcıGiris-1] == "hotmail":
        s = smtplib.SMTP('smtp-mail.outlook.com',587)  #gmail ve hotmail sunucularının smtp adreslerini belirttik
    elif kulllaniciGelen[kullanıcıGiris-1] == "gmail":
        s = smtplib.SMTP('smtp.gmail.com',587)
    s.ehlo()
    s.starttls()
    print("Bağlantı başarıyla kuruldu.")
    print("Giriş yapılıyor...")
    s.login(kullaniciAdi,kullaniciPass) #smtp ile seçime göre outlook veya gmail smtplerine login olmak için kullanıldı.
    print("Giriş başarılı.")
    for i in range(mesajTekrar): #kaç mesaj göndereceğimizi tanımladıktan sonra bu durumu sağlayabilmek adına yazılan kod blokları.
        print("Mesajınız gönderiliyor...")
        s.sendmail(mesajFrom, recipients, mail.as_string())
        print("{}. mesajınız gönderildi.".format(i+1))
    print("Tüm mesajınız başarıyla gönderildi :)")

    print('\n')
    print("1- Maillerini Görüntüle \n 2- Maillerini Sil \n 3- Çıkış \n")
    secim=input("Yukarıdaki seçeneklerden birini seçiniz(Örn 1 veya 2 gibi)  :")
    if secim=='1':
        mailGoruntule()
    if secim=='2':
        mailSilme()
    if secim=='3':
        StopIteration()


#Maillerimizi görüntüledğimiz fonksiyonumuz mailViewdan yapılmıştır.

def mailGoruntule():
    print('Mailleri Görüntüleme İşlemi \n')

    Tk().state("withdrawn")
    kullaniciGelen = ["hotmail","gmail"]
    for option in kullaniciGelen:
        print("{}) {}".format(kullaniciGelen.index(option)+1, option))

    kullaniciGiris = int(input("Kullanmak istediğiniz mail sağlayıcısının sırasını giriniz! (Örn. 1 veya 2): "))

    kullaniciAdi = input("Kullanıcı adınız : ")
    kullaniciPass = input("Şifreniz : ")
    if kullaniciGelen[kullaniciGiris-1] == "hotmail":#mail gönderme fonksiyonunda kullanılan işlem smtp yerine imap adresleri kullanıldı.
        goruntuleBaglanti = imaplib.IMAP4_SSL('imap-mail.outlook.com')
    elif kullaniciGelen[kullaniciGiris-1]=="gmail":
        goruntuleBaglanti=imaplib.IMAP4_SSL('imap.gmail.com')
    print('Bağlantı Kuruluyor...')
    goruntuleBaglanti.login(kullaniciAdi, kullaniciPass) #diğer fonksiyonlardaki gibi mailimize login olmak için imaplibin login ifadesine k.adı şifre parametrelerimizi gönderdik.
    print('Bağlantı Kuruldu...')
    goruntuleBaglanti.list() #mailimizi listelemek için kullandık
    goruntuleBaglanti.select('inbox') #mailden gelen kutumuzu seçtik yani inbox parametresini gönderdik
    print('Lütfen bir süre bekleyiniz...\n')
    result, data = goruntuleBaglanti.uid('search', None, "ALL") # verdiğimiz parametrelerle tüm okunmamışları aramış olduk.
    i = len(data[0].split())



    for x in range(i):
        okunmamisMail = data[0].split()[x]
        result, email_data = goruntuleBaglanti.uid('fetch', okunmamisMail, '(RFC822)') #Parametre olarak RFC822 gönderdik bu sayede okunmamış maillerimizi fetch etmiş oldu.


        raw_email = email_data[0][1]
        raw_email_string = raw_email.decode('utf-8')  #gelen format karışık olduğu ve okunması zor olduğu için utf-8 formatında çevirdik.
        email_message = email.message_from_string(raw_email_string)

        # Başlık detayları için kullandığım kısım
        veri = email.utils.parsedate_tz(email_message['Date'])
        if veri:
            localTarih = datetime.datetime.fromtimestamp(email.utils.mktime_tz(veri))
            localMailDate = "%s" %(str(localTarih.strftime("%a, %d %b %Y %H:%M:%S")))
        emailKimden = str(email.header.make_header(email.header.decode_header(email_message['From'])))  #Bu blokta mailimizin kimden geldiğini 'From' parametresini göndererek email bağlağımızdan decode ettik
        emailKime = str(email.header.make_header(email.header.decode_header(email_message['To']))) #bu blokta yukarıdaki işlemimizin aynısını yaptık fakat gönderdiğimiz parametre from yerine kime kısmını almak için 'to' kullandık.
        emailKonu = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))  #yukarıdaki bloklardaki gibi konuyu çözmek için 'subject' parametresi gönderdik
        print('\n')
        print('Kimden :')
        print(emailKimden)
        print('Kime  :')
        print(emailKime)
        print('Konu :')
        print(emailKonu)
        if emailKonu=='' and emailKimden=='':
            print('Mailiniz Bulunmamaktadır.')
        if kullaniciGelen[kullaniciGiris-1] == "hotmail":
            # Mesaj içerik detaylarını çektiğim kısım
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    mailMetin = part.get_payload(decode=True)
                    dosyaAdi = "email_" + str(x) + ".txt" #gelen maillerimizi .txt uzantısı olarakta kaydetme işlemlerinide yaptık.
                    gelenDosya = open(dosyaAdi, 'w')
                    gelenDosya.write("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s" %(emailKimden, emailKime,localMailDate, emailKonu, mailMetin.decode('utf-8')))
                    gelenDosya.close()

                else:
                    continue
                print('Mesajın İçeriği :\n')
                print(mailMetin)

    print('\n')
    print("1- Mail Gönder \n 2- Maillerini Sil \n 3- Çıkış \n")
    secim=input("Yukarıdaki seçeneklerden birini seçiniz(Örn 1 veya 2 gibi)  :")
    if secim=='1':
        mailGonder()
    if secim=='2':
        mailSilme()
    if secim=='3':
        StopIteration()


#maillerimizi silme işlemlerimizide bu fonksiyon içinde gerçekleştirdik.
def mailSilme():
    print('Maillerinizi Silme İşlemi\n')
    Tk().state("withdrawn")
    kullaniciGelen = ["hotmail","gmail"]
    for option in kullaniciGelen:
        print("{}) {}".format(kullaniciGelen.index(option)+1, option))

    kullaniciGirilen = int(input("Kullanmak istediğiniz mail sağlayıcısının sırasını giriniz! (Örn. 1 veya 2): "))

    kullaniciAdi = input("Kullanıcı adınız : ")
    kullaniciPass = input("Şifreniz : ")

  #görüntüleme ve gönderme işlemiyle aynı fakat kullandığı port numaraları farklı. imap4_ssl kullanıdğımız için

    if kullaniciGelen[kullaniciGirilen-1] == "hotmail":
        silBaglanti = imaplib.IMAP4_SSL('imap-mail.outlook.com', 993)
    elif kullaniciGelen[kullaniciGirilen-1] == "gmail":
        silBaglanti = imaplib.IMAP4_SSL('imap.gmail.com', 993)
    print('Bağlanılıyor...')
    silBaglanti.login(kullaniciAdi,kullaniciPass)
    print('Bağlandı... Lütfen Bekleyiniz...')
    silBaglanti.select('Inbox')
    typ, data = silBaglanti.search(None, 'ALL')
    print('Mailleriniz Siliniyor...')
    for num in data[0].split():
       silBaglanti.store(num, '+FLAGS', '\\Deleted')
    silBaglanti.expunge()
    print('Mailleriniz Silinmiştir...')
    silBaglanti.close() #bağlantımızı kapattığımız kod bloğu
    silBaglanti.logout()
    print('\n')
    print("1- Mail Gönder \n 2- Maillerini Görüntüle \n 3- Maillerini Sil \n 4- Çıkış \n")
    secim=input("Yukarıdaki seçeneklerden birini seçiniz(Örn 1 veya 2 gibi)  :")
    if secim=='1':
        mailGonder()
    if secim=='2':
        mailGoruntule()
    if secim=='4':
        StopIteration() #Programdan çıkmak için kullandığımız kod






def anaMenu():
    print("1- Mail Gönder \n 2- Maillerini Görüntüle \n 3- Maillerini Sil \n 4- Çıkış \n")
    secim=input("Yukarıdaki seçeneklerden birini seçiniz(Örn 1 veya 2 gibi)  :")
    if secim=='1':
        mailGonder()
    if secim=='2':
        mailGoruntule()
    if secim=='3':
        mailSilme()
    if secim=='4':
        StopIteration()

anaMenu()




