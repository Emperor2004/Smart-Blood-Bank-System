"""Notification service for donor mobilization."""
from typing import Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.config import settings


class NotificationService:
    """Service for notification management."""
    
    SMS_TEMPLATE = "Urgent! {hospital_name} needs {blood_group} donors. If eligible, please contact {phone} or click {link}."
    
    def __init__(self, db: Session):
        """Initialize service with database session."""
        self.db = db
        self.sms_enabled = settings.sms_gateway_enabled
        self.email_enabled = settings.email_enabled
        self._twilio_client = None
    
    def _get_twilio_client(self):
        """Lazy load Twilio client."""
        if self._twilio_client is None and self.sms_enabled:
            try:
                from twilio.rest import Client
                self._twilio_client = Client(
                    settings.twilio_account_sid,
                    settings.twilio_auth_token
                )
            except ImportError:
                print("[WARNING] Twilio not installed. Run: pip install twilio")
                self.sms_enabled = False
        return self._twilio_client
    
    def generate_message(self, template_id: str, context: Dict) -> str:
        """Generate notification message from template."""
        if template_id == "donor_mobilization":
            return self.SMS_TEMPLATE.format(**context)
        else:
            raise ValueError(f"Unknown template: {template_id}")
    
    def send_sms(self, phone: str, message: str) -> bool:
        """Send SMS via Twilio gateway."""
        if self.sms_enabled:
            try:
                client = self._get_twilio_client()
                if client:
                    msg = client.messages.create(
                        body=message,
                        from_=settings.twilio_phone_number,
                        to=phone
                    )
                    print(f"[SMS SENT] SID: {msg.sid}, To: {phone}")
                    return True
                else:
                    print(f"[SMS SIMULATION] To: {phone}, Message: {message}")
                    return True
            except Exception as e:
                print(f"[SMS ERROR] {str(e)}")
                return False
        else:
            print(f"[SMS SIMULATION] To: {phone}, Message: {message}")
            return True
    
    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send email notification."""
        if self.email_enabled:
            try:
                import smtplib
                from email.mime.text import MIMEText
                from email.mime.multipart import MIMEMultipart
                
                msg = MIMEMultipart()
                msg['From'] = settings.email_from
                msg['To'] = to_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))
                
                with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
                    server.starttls()
                    server.login(settings.smtp_user, settings.smtp_password)
                    server.send_message(msg)
                
                print(f"[EMAIL SENT] To: {to_email}")
                return True
            except Exception as e:
                print(f"[EMAIL ERROR] {str(e)}")
                return False
        else:
            print(f"[EMAIL SIMULATION] To: {to_email}, Subject: {subject}")
            return True
    
    def log_notification(self, donor_id: int, template_id: str, message: str, status: str) -> Notification:
        """Log notification to database."""
        notification = Notification(
            donor_id=donor_id,
            template_id=template_id,
            message=message,
            status=status,
            sent_at=datetime.now() if status == "sent" else None
        )
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification
    
    def notify_donor(self, donor_id: int, donor_phone: str, hospital_name: str, 
                     blood_group: str, contact_phone: str, contact_link: str = "#") -> Dict:
        """Send notification to donor."""
        context = {
            "hospital_name": hospital_name,
            "blood_group": blood_group,
            "phone": contact_phone,
            "link": contact_link
        }
        
        message = self.generate_message("donor_mobilization", context)
        
        try:
            success = self.send_sms(donor_phone, message)
            status = "sent" if success else "failed"
        except Exception as e:
            status = "failed"
            print(f"Failed to send SMS: {str(e)}")
        
        if not self.sms_enabled:
            status = "simulated"
        
        notification = self.log_notification(donor_id, "donor_mobilization", message, status)
        
        return {
            "notification_id": notification.notification_id,
            "donor_id": donor_id,
            "status": status,
            "message": message,
            "sent_at": notification.sent_at
        }
    
    def get_notifications(self, donor_id: Optional[int] = None, status: Optional[str] = None) -> list:
        """Get notification records."""
        query = self.db.query(Notification)
        
        if donor_id:
            query = query.filter(Notification.donor_id == donor_id)
        if status:
            query = query.filter(Notification.status == status)
        
        return query.order_by(Notification.created_at.desc()).all()
