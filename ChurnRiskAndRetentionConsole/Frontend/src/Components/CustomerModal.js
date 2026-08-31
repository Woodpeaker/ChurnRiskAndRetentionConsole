import * as React from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import Button from '@mui/material/Button';

const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: '80%',
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
};

export default function CustomerModal({ open, handleClose, customerId }) {
    const [customerData, setCustomerData] = React.useState(null);
    const [outreachStatus, setOutreachStatus] = React.useState(null);
    const onHandleOutreachClick = () => {
        fetch(`/customers/${customerId}/outreach`, {
            method: 'PATCH'
        })
        .then((response) => response.json())
        .then((data) => {
            const newData = { ...customerData, outreach: data.outreach };
            setCustomerData(newData);
            setOutreachStatus(data.outreach);
        })
        .catch((error) => console.error('Error updating outreach status:', error));
    };
    async function fetchCustomerData() {
        try {
            const response = await fetch(`/customers/${customerId}`);
            const data = await response.json();
            setCustomerData(data);
            setOutreachStatus(data.outreach);
        } catch (error) {
            console.error('Error fetching customer data:', error);
        }
    }
    React.useEffect(() => {
        if (customerId && open) {
            // Fetch customer data from the backend
            fetchCustomerData();
        }
    }, [customerId, open]);

    let OutreachButton;
    if (outreachStatus === 'Not Contacted') {
        OutreachButton = (
            <Button variant="outlined" size="medium" onClick={() => onHandleOutreachClick()}>
                Contact Customer
            </Button>
        );
    }
    else if (outreachStatus === 'In Progress') {
        OutreachButton = (
            <Button variant="outlined" size="medium" onClick={() => onHandleOutreachClick()}>
                Resolve Outreach
            </Button>
        );
    }
    else if (outreachStatus === 'Resolved') {
        OutreachButton = (
            <Button variant="outlined" size="medium" disabled>
                done
            </Button>
        );
    }

    return (
        <Modal
            open={open}
            onClose={handleClose}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
        >
            <Box sx={style}>
                {customerData ? (
                    <Box>
                        <Typography id="modal-modal-title" variant="h5" component="h2">
                            Customer Details : {customerData.customer_id}
                        </Typography>
                        <Typography id="modal-modal-title" variant="h6" component="h2">
                            {outreachStatus}
                        </Typography>
                        {OutreachButton}
                        <List
                            rowHeight={46}
                            rowCount={200}
                            style={{
                            height: 400,
                            overflow: 'auto'
                        }}>
                            <ListItem>
                                <ListItemText
                                    primary="Customer ID"
                                    secondary={customerData.customer_id}
                                />
                            </ListItem>
                            {Object.entries(customerData).map(([key, value]) => (
                                <ListItem key={key}>
                                    <ListItemText
                                        primary={key.replace(/_/g, ' ').replace(/\b\w/g, (l) => l.toUpperCase())}
                                        secondary={value}
                                    />
                                </ListItem>
                            ))}
                        </List>
                    </Box>
                ) : (
                    <Typography>Loading...</Typography>
                )}
            </Box>
        </Modal>
    );
}
