import { useState, useEffect, useCallback } from 'react';

export const useMiningData = (walletAddress) => {
    const [miningData, setMiningData] = useState({
        btc_bal: 0,
        blocks: 0,
        eth_price: 0,
        ltc_price: 0,
        isLive: false
    });

    // Pull the API URL securely from the environment
    const apiUrl = process.env.REACT_APP_API_URL || 'http://127.0.0.1:5000';

    const fetchEnginePulse = useCallback(async () => {
        if (!walletAddress) return; // Prevent fetching if wallet isn't loaded

        try {
            const response = await fetch(`${apiUrl}/api/data`);
            const data = await response.json();
            
            if (!data.error) {
                setMiningData({
                    btc_bal: data.btc_bal,
                    blocks: data.blocks,
                    eth_price: data.eth_price,
                    ltc_price: data.ltc_price,
                    isLive: true
                });
            }
        } catch (error) {
            console.error("[ERROR] Termux API Bridge Offline.");
            setMiningData(prev => ({ ...prev, isLive: false }));
        }
    }, [apiUrl, walletAddress]); // [CRITICAL FIX]: Dependencies added to prevent stale closures

    useEffect(() => {
        // Initial fetch
        fetchEnginePulse();

        // Establish the polling interval
        const interval = setInterval(fetchEnginePulse, 5000);

        // Cleanup memory on unmount
        return () => clearInterval(interval);
    }, [fetchEnginePulse]); // [CRITICAL FIX]: useCallback function passed as dependency

    return miningData;
};
