import * as React from 'react';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material/styles';
import MobileStepper from '@mui/material/MobileStepper';
import Paper from '@mui/material/Paper';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import KeyboardArrowLeft from '@mui/icons-material/KeyboardArrowLeft';
import KeyboardArrowRight from '@mui/icons-material/KeyboardArrowRight';

// Steps will be driven by the riskInformations fetched from the backend.

export default function CustomStepper() {
    const theme = useTheme();
    const [activeStep, setActiveStep] = React.useState(0);
    const [riskInformations, setRiskInformations] = React.useState([]);
    const [loading, setLoading] = React.useState(true);
    const [fetchError, setFetchError] = React.useState(null);
    // Use fetched risk information as the dynamic steps. Ensure at least one step
    // so the UI remains stable while data is loading.
    const maxSteps = Math.max(riskInformations.length, 1);

    const handleNext = () => {
        setActiveStep((prevActiveStep) => prevActiveStep + 1);
    };

    const handleBack = () => {
        setActiveStep((prevActiveStep) => prevActiveStep - 1);
    };

    const nextButtonRef = React.useRef(null);
    const backButtonRef = React.useRef(null);
    const previousActiveStepRef = React.useRef(activeStep);

    // Manage focus when the active step changes and fetch risk information.
    React.useEffect(() => {
        const previousActiveStep = previousActiveStepRef.current;
        previousActiveStepRef.current = activeStep;

        let mounted = true;
        (async () => {
            setLoading(true);
            setFetchError(null);
            try {
                const response = await fetch(`/model/info`, {
                    method: 'GET',
                    headers: { Accept: 'application/json' },
                });
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const data = await response.json();
                // Normalize to an array of risk information objects.
                let list = [];
                if (Array.isArray(data)) {
                    list = data;
                } else if (data && typeof data === 'object') {
                    // If the server returns an object with an items property, use it.
                    if (Array.isArray(data.items)) list = data.items;
                    else list = Object.values(data);
                }
                if (mounted) setRiskInformations(list);
            } catch (err) {
                console.error('Failed to fetch risk information', err);
                if (mounted) setFetchError(err.message || 'Fetch error');
                if (mounted) setRiskInformations([]);
            } finally {
                if (mounted) setLoading(false);
            }
        })();
        if (activeStep === 0 && previousActiveStep === 1) {
            // If the user is going back to the first step, focus the "Next" button.
            nextButtonRef.current.focus();
            return;
        }

        if (activeStep === maxSteps - 1 && previousActiveStep === maxSteps - 2) {
            // If the user is going to the last step, focus the "Back" button.
            backButtonRef.current.focus();
        }
    }, [activeStep, maxSteps]);

    // If the fetched data has fewer steps than the current activeStep, clamp it.
    React.useEffect(() => {
        if (riskInformations.length > 0 && activeStep > riskInformations.length - 1) {
            setActiveStep(Math.max(0, riskInformations.length - 1));
        }
    }, [riskInformations]);

    return (
        <Box sx={{ maxWidth: 400, flexGrow: 1 }}>
            <Paper
                square
                elevation={0}
                sx={{
                    display: 'flex',
                    alignItems: 'center',
                    height: 50,
                    pl: 2,
                    bgcolor: 'background.default',
                }}
            >

                <Typography>
                    {loading
                        ? 'Loading...'
                        : fetchError
                            ? `Error: ${fetchError}`
                            : riskInformations[activeStep]?.risk_name || 'No risk information'}
                </Typography>
            </Paper>
            <Box sx={{ height: 100, maxWidth: 400, width: '100%', p: 2 }}>
                {loading
                    ? 'Loading details...'
                    : fetchError
                        ? 'Unable to load details.'
                        : riskInformations[activeStep]?.risk_breakdown || 'No details available.'}
            </Box>
            <MobileStepper
                variant="text"
                steps={maxSteps}
                position="static"
                activeStep={activeStep}
                nextButton={
                    <Button
                        size="small"
                        onClick={handleNext}
                        disabled={loading || riskInformations.length === 0 || activeStep === maxSteps - 1}
                        ref={nextButtonRef}
                    >
                        Next
                        {theme.direction === 'rtl' ? (
                            <KeyboardArrowLeft />
                        ) : (
                            <KeyboardArrowRight />
                        )}
                    </Button>
                }
                backButton={
                    <Button
                        size="small"
                        onClick={handleBack}
                        disabled={loading || activeStep === 0}
                        ref={backButtonRef}
                    >
                        {theme.direction === 'rtl' ? (
                            <KeyboardArrowRight />
                        ) : (
                            <KeyboardArrowLeft />
                        )}
                        Back
                    </Button>
                }
            />
        </Box>
    );
}
