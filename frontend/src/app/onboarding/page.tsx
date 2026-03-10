import ProtectedRoute from "@/components/auth/ProtectedRoute";

const Onboarding = () => {
    return (
        <ProtectedRoute>
            <div>
                <h1>Begin Onboarding</h1>
            </div>
        </ProtectedRoute>
    )
}

export default Onboarding;