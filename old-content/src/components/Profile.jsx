import { useAuth0 } from '@auth0/auth0-react';
import './Profile.css';

const Profile = () => {
    const { user, isAuthenticated } = useAuth0();

    return (
        isAuthenticated && (
            <article className='column'>
                {user?.picture && <img src={user.picture} alt={user?.name} />}
                <h2 className='name'>{user?.name}</h2>
                <ul className='attribute-list'>
                    {Object.entries(user).map(([key, value]) => (
                        <li key={key} className='attribute'>
                            <span className='attribute-name'>{key}:</span>
                            <span className='attribute-value'>{value}</span>
                        </li>
                    ))}
                </ul>
            </article>
        )
    );
};

export default Profile;
