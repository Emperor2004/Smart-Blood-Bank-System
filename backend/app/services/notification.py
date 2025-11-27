"""Notification service for donor mobilization."""
from typing import Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.notification import Notification
from app.config import settings


class NotificationService:
    """Service for notification management."""
    
    # SMS template
    SMS_TEMPLATE = "Urgent! {hospital_name} needs {blood_group} donors. If eligible, please contact {phone} or click {link}."
    
    def __init__(self, db: Session):
        """Initialize service with database session."""
        self.db = db
        self.sms_enabled = settings.sms_gateway_enabled
    
    def generate_message(
        self,
        template_id: str,
        context: Dict
    ) -> str:
        """
        Generate notification message from template.
        
        Args:
            template_id: Template identifier
            context: Context dictionary with placeholder values
            
        Returns:
            Generated message
        """
        if template_id == "donor_mobilization":
            return self.SMS_TEMPLATE.format(**context)
        else:
            raise ValueError(f"Unknown template: {template_id}")
    
    def send_sms(self, phone: str, message: str) -> bool:
        """
        Send SMS via gateway.
        
        Args:
            phone: Phone number
            message: Message text
            
        Returns:
            True if sent successfully
        """
        if self.sms_enabled:
            # TODO: Integrate with actual SMS gateway (Twilio/AWS SNS)
            # For now, simulate
            print(f"[SMS SIMULATION] To: {phone}, Message: {message}")
            return True
        else:
            # Simulation mode
            print(f"[SMS SIMULATION] To: {phone}, Message: {message}")
            return True
    
    def log_notification(
        self,
        donor_id: int,
        template_id: str,
        message: str,
        status: str
    ) -> Notification:
        """
        Log notification to database.
        
        Args:
            donor_id: Donor ID
            template_id: Template identifier
            message: Message text
            status: Notification status
            
        Returns:
            Created notification record
        """
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
    
    def notify_donor(
        self,
        donor_id: int,
        donor_phone: str,
        hospital_name: str,
        blood_group: str,
        contact_phone: str,
        contact_link: str = "#"
    ) -> Dict:
        """
        Send notification to donor.
        
        Args:
            donor_id: Donor ID
            donor_phone: Donor phone number
            hospital_name: Hospital name
            blood_group: Blood group needed
            contact_phone: Hospital contact phone
            contact_link: Contact link
            
        Returns:
            Notification result
        """
        # Generate message
        context = {
            "hospital_name": hospital_name,
            "blood_group": blood_group,
            "phone": contact_phone,
            "link": contact_link
        }
        
        message = self.generate_message("donor_mobilization", context)
        
        # Send SMS
        try:
            success = self.send_sms(donor_phone, message)
            status = "sent" if success else "failed"
        except Exception as e:
            status = "failed"
            print(f"Failed to send SMS: {str(e)}")
        
        # If SMS gateway not enabled, mark as simulated
        if not self.sms_enabled:
            status = "simulated"
        
        # Log notification
        notification = self.log_notification(
            donor_id=donor_id,
            template_id="donor_mobilization",
            message=message,
            status=status
        )
        
        return {
            "notification_id": notification.notification_id,
            "donor_id": donor_id,
            "status": status,
            "message": message,
            "sent_at": notification.sent_at
        }
    
    def get_notifications(
        self,
        donor_id: Optional[int] = None,
        status: Optional[str] = None
    ) -> list:
        """
        Get notification records.
        
        Args:
            donor_id: Optional donor ID filter
            status: Optional status filter
            
        Returns:
            List of notification records
        """
        query = self.db.query(Notification)
        
        if donor_id:
            query = query.filter(Notification.donor_id == donor_id)
        if status:
            query = query.filter(Notification.status == status)
        
        return query.order_by(Notification.created_at.desc()).all()
