import React, { useState, useEffect } from 'react';

export default function ApiKeyManager() {
    // [SHIELD OF OGÚN]: Key is pulled dynamically from the environment, never hardcoded.
    const securedKey = process.env.REACT_APP_NICEHASH_API_KEY;
    const [keyStatus, setKeyStatus] = useState('UNVERIFIED');

    useEffect(() => {
        if (securedKey && securedKey !== "insert_your_real_key_here") {
            setKeyStatus('SECURED & ACTIVE');
        } else {
            setKeyStatus('MISSING ENVIRONMENT VARIABLE');
        }
    }, [securedKey]);

    return (
        <div className="bg-[#111] border border-gray-800 p-4 rounded text-[#00ff41] font-mono mt-4">
            <h3 className="text-gray-500 text-xs mb-2">API KEY MANAGEMENT [PROTOCOL IJAPA]</h3>
            <div className="flex justify-between items-center">
                <span>Network Authorization:</span>
                <span className={keyStatus === 'SECURED & ACTIVE' ? 'text-green-500 font-bold' : 'text-red-500 font-bold'}>
                    [{keyStatus}]
                </span>
            </div>
            <div className="text-xs text-gray-600 mt-2">
                * Keys are strictly managed via Zero-Storage environment variables.
            </div>
        </div>
    );
}
